from uuid import uuid4
from api.v1.weixinapp_resource import WeixinAppResource

from django.conf.urls import url
from tastypie import fields
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.http import HttpUnauthorized, HttpBadRequest
from tastypie.throttle import CacheThrottle
from weixin.models import PublicAccount, PublicAccountApp
from weixin.utils import Weixin
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

    def dehydrate_apps(self, bundle):
        public_account_apps =  PublicAccountApp.objects.filter(public_account = bundle.obj)
        result = []
        for pa in public_account_apps:
            app_resource = WeixinAppResource()
            bundle = app_resource.build_bundle(obj=pa.app, request=bundle.request)
            result.append(app_resource.full_dehydrate(bundle))

        return result

    def prepend_urls(self):
        return [
            url(r'^publicaccount/auto/$',
                self.wrap_view('auto'), name='api_weixin_auto'),
        ]

    def auto(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        apikey_auth = ApiKeyAuthentication()
        if apikey_auth.is_authenticated(request) == True:
            data = self.deserialize(request, request.body,
                                    format=request.META.get('CONTENT_TYPE', 'application/json'))
            username = data.get('username', None)
            password = data.get('password', None)
            try:
                w = Weixin(username, password)
                w.login()
                user_dict = w.get_user_info()
                public_account = PublicAccount.objects.get_or_create(
                    user=request.user,
                    type=user_dict['type'],
                    title=user_dict['title'],
                    weixin_id=user_dict['weixin_id'],
                    thumbnail_url=request.build_absolute_uri(user_dict['thumbnail_url'])
                )[0]
                public_account.save()
                bundle = self.build_bundle(obj=public_account, request=request)
                bundle = self.full_dehydrate(bundle)
                return self.create_response(request, bundle)
            except Exception as e:
                return self.obj_create(request, {}, HttpBadRequest)

        else:
            return self.create_response(request, {}, HttpUnauthorized)

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
