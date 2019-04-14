from account.models import Account
from django.core.exceptions import ObjectDoesNotExist
from payments.models import Customer

from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle

from tastypie.exceptions import Unauthorized
from tastypie.fields import ToOneField, CharField, IntegerField, ToManyField, DateTimeField
from tastypie.resources import ModelResource, Resource
from tastypie.utils import now

from dds.authorizations import OwnedOnlyAuthorization, SelfOnlyAuthorization
from dds.models import CensusField, Query, QueryFilter, ExportJob
from dds.validators import QueryFilterValidation


class CensusFieldResource(ModelResource):
    class Meta:
        exclude = ['indexed']
        queryset = CensusField.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()


class ExportJobResource(ModelResource):
    query = ToOneField('dds.api.QueryResource', attribute='query')
    requested = DateTimeField('requested', readonly=True, default=now)
    begin = DateTimeField('begin', readonly=True, null=True, blank=True)
    end = DateTimeField('end', readonly=True, null=True, blank=True)
    download_link = CharField('get_indirect_link', readonly=True, blank=True)
    filename = CharField('export_filename', readonly=True, blank=True, null=True)
    class Meta:
        queryset = ExportJob.objects.all()
        authentication = SessionAuthentication()
        authorization = OwnedOnlyAuthorization()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(query__account=request.user.account)

    def obj_create(self, bundle, **kwargs):
        result = super(ExportJobResource, self).obj_create(bundle, **kwargs)
        if result.obj.query.account != bundle.request.user.account: raise Unauthorized("Can't attach to a query that is not yours")
        return result

    def obj_get_list(self, bundle, **kwargs):
        return [f for f in super(ExportJobResource, self).obj_get_list(bundle, **kwargs) if f.query.account == bundle.request.user.account]

    def obj_get(self, bundle, **kwargs):
        result = super(ExportJobResource, self).obj_get(bundle, **kwargs)
        if result.query.account != bundle.request.user.account: raise Unauthorized("Forbidden")
        return result


class QueryResource(ModelResource):
    sample = CharField(attribute='sample', readonly=True, null=True, help_text="sample of the data returned")
    num_records = IntegerField(attribute='num_records', readonly=True, help_text="number of records matched")
    sort_by = ToOneField(CensusFieldResource, attribute='sort_by', help_text="field to sort results by")
    queryfilter_set = ToManyField('dds.api.QueryFilterResource', attribute='queryfilter_set', blank=True, null=True, full=True)
    export_jobs = ToManyField(ExportJobResource, attribute='exportjob_set', help_text="jobs run with this query", full=True, blank=True, null=True)

    class Meta:
        queryset = Query.objects.all()
        authentication = SessionAuthentication()
        authorization = OwnedOnlyAuthorization()

    def obj_create(self, bundle, **kwargs):
        return super(QueryResource, self).obj_create(bundle, account=bundle.request.user.account, **kwargs)

    def obj_get_list(self, bundle, **kwargs):
        return [f for f in super(QueryResource, self).obj_get_list(bundle, **kwargs) if f.account == bundle.request.user.account]

    def obj_get(self, bundle, **kwargs):
        result = super(QueryResource, self).obj_get(bundle, **kwargs)
        if result.account != bundle.request.user.account: raise Unauthorized("Forbidden")
        return result

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(account=request.user.account)


class QueryFilterResource(ModelResource):
    query = ToOneField(QueryResource, attribute='query', help_text="query to which the filter belongs")
    field = ToOneField(CensusFieldResource, attribute='field', help_text="field by which to filter")

    class Meta:
        queryset = QueryFilter.objects.all()
        authentication = SessionAuthentication()
        authorization = OwnedOnlyAuthorization()
        validation = QueryFilterValidation()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(query__account=request.user.account)

    def obj_create(self, bundle, **kwargs):
        result = super(QueryFilterResource, self).obj_create(bundle, **kwargs)
        if result.obj.query.account != bundle.request.user.account: raise Unauthorized("Can't attach to a query that is not yours")
        return result

    def obj_get_list(self, bundle, **kwargs):
        return [f for f in super(QueryFilterResource, self).obj_get_list(bundle, **kwargs) if f.query.account == bundle.request.user.account]

    def obj_get(self, bundle, **kwargs):
        result = super(QueryFilterResource, self).obj_get(bundle, **kwargs)
        if result.query.account != bundle.request.user.account: raise Unauthorized("Forbidden")
        return result


class AccountResource(ModelResource):
    queries = ToManyField(QueryResource, readonly=True, attribute='query_set', help_text="query to which the filter belongs", full=True)
    detail_allowed_methods = ['get']
    list_allowed_methods = []

    class Meta:
        queryset = Account.objects.all()
        authentication = SessionAuthentication()
        authorization = SelfOnlyAuthorization()

    def obj_get(self, bundle, **kwargs):
        result = super(AccountResource, self).obj_get(bundle, **kwargs)
        if result != bundle.request.user.account: raise Unauthorized("Forbidden")
        return result


class SubscriptionResource(Resource):
    class Meta:
        authentication = SessionAuthentication()
        authorization = Authorization()

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id

        return kwargs

    def get_object_list(self, request):
        try:
            return [request.user.customer.current_subscription]
        except ObjectDoesNotExist:
            return []

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        return bundle.request.user.customer.current_subscription

    def obj_create(self, bundle, **kwargs):
        try:
            customer = bundle.request.user.customer
        except ObjectDoesNotExist:
            customer = Customer.create(bundle.request.user)
        customer.update_card(bundle.data["stripe_token"])
        customer.subscribe(bundle.data["plan_type"])


    def obj_delete(self, bundle, **kwargs):
        bundle.request.user.customer.cancel(False)

    def rollback(self, bundles):
        pass