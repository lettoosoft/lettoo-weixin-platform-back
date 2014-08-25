from tastypie import fields
from tastypie.authentication import MultiAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie.throttle import CacheThrottle
from weixin.models import App
from .base import MyBaseResource
from .user import UserResource


class WeixinAppAuthorization(Authorization):
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

        return model_klass

    def read_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)

        if klass is False:
            return []

        object_list = object_list.filter(published=True)

        # GET-style methods are always allowed.
        return object_list


class WeixinAppResource(MyBaseResource):
    creator = fields.ForeignKey(UserResource, 'user', full=True, readonly=True, null=True)
    screen_shots = fields.ApiField('screen_shots', null=True, readonly=True)

    class Meta:
        always_return_data = True
        detail_allowed_methods = ['get', ]
        list_allowed_methods = ['get']
        resource_name = 'weixinapp'
        queryset = App.objects.filter(published=True).order_by('-created')
        authentication = MultiAuthentication(Authentication())
        authorization = WeixinAppAuthorization()
        excludes = ['modified']
        ordering = ['created']
        throttle = CacheThrottle(throttle_at=600)

    def dehydrate_screen_shots(self, bundle):
        attachments =  bundle.obj.attachments
        for d in attachments:
            if not (d['url'].startswith('http://') or d['url'].startswith('https://')):
                d['url'] = bundle.request.build_absolute_uri(d['url'])
        return attachments
