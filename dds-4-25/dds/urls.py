from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from tastypie.api import Api

from dds.api import QueryResource, QueryFilterResource, CensusFieldResource, AccountResource, SubscriptionResource, ExportJobResource
from dds.views import homepage, get_exported_file


api = Api(api_name='api')
api.register(CensusFieldResource())
api.register(QueryFilterResource())
api.register(QueryResource())
api.register(AccountResource())
api.register(ExportJobResource())

payments_api = Api(api_name='payments')
payments_api.register(SubscriptionResource())

urlpatterns = patterns("",
                       url(r"^$", homepage, name='home'),
                       url(r"^exported_file/(?P<filename>[\w\d.]+)$", get_exported_file),
                       url(r"^admin/", include(admin.site.urls)),
                       url(r"^account/", include("account.urls")),
                       url(r"^payments/", include("payments.urls")),
                       url(r'^', include(payments_api.urls)),
                       url(r'^', include(api.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
