from django.conf.urls import url

from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.http import HttpBadRequest, HttpUnauthorized
from tastypie.throttle import CacheThrottle

from attachment.models import Attachment
from .base import MyBaseResource


class AttachmentAuthorization(Authorization):
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

        # GET-style methods are always allowed.
        return object_list

    def read_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized('You are not allowed to access that resource.')

        # GET-style methods are always allowed.
        return True


class AttachmentResource(MyBaseResource):
    class Meta:
        always_return_data = True
        detail_allowed_methods = ['get', 'put', 'post', 'delete']
        list_allowed_methods = ['get', 'post']
        resource_name = 'attachment'
        queryset = Attachment.objects.all().order_by('-created')
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = AttachmentAuthorization()
        excludes = ['modified']
        ordering = ['created']
        throttle = CacheThrottle(throttle_at=600)

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>attachment)/upload/$',
                self.wrap_view('attachment_upload'), name='attachment_upload'),
        ]

    def obj_create(self, bundle, **kwargs):
        return super(AttachmentResource, self).obj_create(bundle, user=bundle.request.user)

    def attachment_upload(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        apikey_auth = ApiKeyAuthentication()
        if apikey_auth.is_authenticated(request) == True:
            if request.user.is_staff:
                if 'multipart/form-data' not in str(request.META['CONTENT_TYPE']):
                    return self.create_response(request, {
                        'error': 'Unsupported media type',
                    }, HttpBadRequest)
                else:
                    if ('file' in request.FILES):
                        file = request.FILES['file']
                        name = request.POST.get('name', file.name)
                        attachment = Attachment(user=request.user, name=name, file=file)
                        attachment.save()

                        return self.create_response(
                            request,
                            {'id': attachment.id, 'url': request.build_absolute_uri(attachment.file.url)})
                    else:
                        return self.create_response(request, {
                            'error': 'No file found',
                        }, HttpBadRequest)
        else:
            return self.create_response(request, {}, HttpUnauthorized)
