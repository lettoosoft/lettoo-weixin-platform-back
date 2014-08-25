from django.conf.urls import patterns, include, url
from tastypie.api import Api

from .v1.user import UserResource, CreateUserResource
from .v1.weixin_resource import PublicAccountResource
from .v1.attachment_resource import AttachmentResource


v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(CreateUserResource())
v1_api.register(PublicAccountResource())
v1_api.register(AttachmentResource())

urlpatterns = patterns('',
                       url(r'', include(v1_api.urls)),
)
