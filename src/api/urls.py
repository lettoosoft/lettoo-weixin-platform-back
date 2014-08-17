from django.conf.urls import patterns, include, url
from tastypie.api import Api

from .v1.user import UserResource, CreateUserResource
from .v1.weixin_resource import PublicAccountResource


v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(CreateUserResource())
v1_api.register(PublicAccountResource())

urlpatterns = patterns('',
                       url(r'', include(v1_api.urls)),
)
