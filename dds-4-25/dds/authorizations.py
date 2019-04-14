from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class OwnedOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return [o for o in object_list if o.is_owned_by(bundle.request.user)]

    def read_detail(self, object_list, bundle):
        return bundle.obj.is_owned_by(bundle.request.user)

    def create_list(self, object_list, bundle):
        return [o for o in object_list if o.is_owned_by(bundle.request.user)]

    def create_detail(self, object_list, bundle):
        return bundle.obj.is_owned_by(bundle.request.user)

    def update_list(self, object_list, bundle):
        return [o for o in object_list if o.is_owned_by(bundle.request.user)]

    def update_detail(self, object_list, bundle):
        return bundle.obj.is_owned_by(bundle.request.user)

    def delete_list(self, object_list, bundle):
        return [o for o in object_list if o.is_owned_by(bundle.request.user)]

    def delete_detail(self, object_list, bundle):
        return bundle.obj.is_owned_by(bundle.request.user)


class SelfOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return not bundle.obj.id or bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        raise Unauthorized("Creation not permitted")

    def create_detail(self, object_list, bundle):
        raise Unauthorized("Creation not permitted")

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Deletion not permitted")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Deletion not permitted")