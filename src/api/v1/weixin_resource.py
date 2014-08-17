from uuid import uuid4

from tastypie import fields
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.throttle import CacheThrottle
from weixin.models import PublicAccount
from .base import MyBaseResource
from .user import UserResource


class PublicAccountAuthorization(Authorization):
    '''
    Uses permission checking from ``django.contrib.auth`` to map
    ``POST / PUT / DELETE / PATCH`` to their equivalent Django auth
    permissions.

    Both the list & detail variants simply check the model they're based
    on, as that's all the more granular Django's permission setup gets.
    '''

    def base_checks(self, request, model_klass):
        # If it doesn't look like a model, we can't check permissions.
        if not model_klass or not getattr(model_klass, '_meta', None):
            return False

        # User must be logged in to check permissions.
        if not hasattr(request, 'user'):
            return False

        return model_klass

    def read_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)

        if klass is False:
            return []

        object_list = object_list.filter(user=bundle.request.user)

        # GET-style methods are always allowed.
        return object_list

    def read_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized('You are not allowed to access that resource.')

        if bundle.obj.user != bundle.request.user:
            raise Unauthorized('You are not allowed to access that resource.')

        # GET-style methods are always allowed.
        return True

    def create_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized('You are not allowed to access that resource.')

        return True

    def update_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized('You are not allowed to access that resource.')

        if bundle.obj.user != bundle.request.user:
            raise Unauthorized('You are not allowed to access that resource.')

        return True

    def delete_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized('You are not allowed to access that resource.')

        if bundle.obj.user != bundle.request.user:
            raise Unauthorized('You are not allowed to access that resource.')

        return True


class PublicAccountResource(MyBaseResource):
    user = fields.ForeignKey(UserResource, 'user', full=True, readonly=True, null=True)
    apps = fields.ApiField('apps', null=True, readonly=True)

    class Meta:
        always_return_data = True
        detail_allowed_methods = ['get', 'put', 'post', 'delete']
        list_allowed_methods = ['get', 'post']
        resource_name = 'publicaccount'
        queryset = PublicAccount.objects.all().order_by('-created')
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = PublicAccountAuthorization()
        excludes = ['modified']
        ordering = ['created']
        throttle = CacheThrottle(throttle_at=600)

    def obj_create(self, bundle, **kwargs):
        # contact = MiniContact.objects.get_or_create_contact(bundle.obj.event.creator, bundle.request.user.email)
        user = bundle.request.user
        token = uuid4().hex
        return super(PublicAccountResource, self).obj_create(
            bundle,
            user=user,
            token=token,
            callback_url=bundle.request.build_absolute_uri('/weixin/%d/%s/' % (user.id, token ))
        )
