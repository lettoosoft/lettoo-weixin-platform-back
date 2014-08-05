from tastypie.api import Api

from .v1.user import UserResource, CreateUserResource


v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(CreateUserResource())
