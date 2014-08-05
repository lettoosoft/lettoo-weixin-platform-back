import json

from django.conf.urls import url
from django.contrib.auth import user_logged_in, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from tastypie import fields, http
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized, BadRequest
from tastypie.http import HttpUnauthorized, HttpBadRequest
from tastypie.models import ApiKey
from tastypie.utils import dict_strip_unicode_keys
from account.forms import ChangePasswordForm, SetPasswordForm
from account.models import EmailConfirmation
from account.utils import send_reset_password_email
from userprofile.models import AvatarPhoto
from userprofile.utils import check_user_profile, handle_user_profile
from socialaccount.models import GOOGLE, SocialApp, FACEBOOK, SocialToken
from socialaccount.utils import GoogleAdapter, FacebookAdapter
from ..utils import check_user
from .base import MyBaseResource


class UserAuthorization(Authorization):
    def base_checks(self, request, model_klass):
        # If it doesn't look like a model, we can't check permissions.
        if not model_klass or not getattr(model_klass, '_meta', None):
            raise Unauthorized('You are not allowed to access this resource.')

        return model_klass

    def read_detail(self, object_list, bundle):
        self.base_checks(bundle.request, bundle.obj.__class__)

        if not bundle.obj.id == bundle.request.user.id:
            raise Unauthorized('You are not allowed to access this resource.')

        return True


class UserResource(MyBaseResource):
    profile = fields.ApiField(attribute='profile', null=True, blank=True, readonly=True)
    has_usable_password = fields.BooleanField(attribute='has_usable_password', null=True, blank=True, readonly=True)
    email_verified = fields.BooleanField(attribute='email_verified', null=True, blank=True, readonly=True)

    class Meta:
        always_return_data = True
        detail_allowed_methods = ['get', 'put', 'delete']
        list_allowed_methods = []
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = UserAuthorization()
        excludes = ['is_active', 'is_staff', 'is_superuser', 'password']

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        bundle = super(UserResource, self).obj_update(bundle, skip_errors, **kwargs)
        handle_user_profile(bundle.obj, bundle.data)
        apikey = ApiKey.objects.get_or_create(user=bundle.obj)[0].key
        bundle.data['apikey'] = apikey
        social_access_token = SocialToken.get_user_tokens(bundle.obj)
        if social_access_token:
            bundle.data['social_access_token'] = social_access_token
        # bundle.data['social_access_token'] = SocialToken.get_user_tokens(bundle.obj)
        return bundle

    def dehydrate_profile(self, bundle):
        return bundle.obj.profile.extra_data

    def dehydrate_has_usable_password(self, bundle):
        return bundle.obj.has_usable_password()

    def dehydrate_email_verified(self, bundle):
        try:
            ec = EmailConfirmation.objects.get(user=bundle.obj)
            return ec.verified
        except EmailConfirmation.DoesNotExist:
            return True

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>user)/google/login/$',
                self.wrap_view('google_login'), name='api_google_login'),

            url(r'^(?P<resource_name>user)/facebook/login/$',
                self.wrap_view('facebook_login'), name='api_facebook_login'),

            url(r'^(?P<resource_name>user)/login/$',
                self.wrap_view('login'), name='api_login'),

            url(r'^(?P<resource_name>user)/password/reset/$',
                self.wrap_view('reset_password'), name='reset_password'),

            url(r'^(?P<resource_name>user)/password/change/$',
                self.wrap_view('change_password'), name='change_password'),

            url(r'^(?P<resource_name>user)/avatarupload/$',
                self.wrap_view('avatar_upload'), name='avatar_upload'),

            url(r'^(?P<resource_name>user)/disconnect/(?P<provider>\w+)/$',
                self.wrap_view('disconnect_socialaccount'), name='disconnect_socialaccount'),
        ]

    def disconnect_socialaccount(self, request, provider, **kwargs):
        self.method_check(request, allowed=['post'])

        apikey_auth = ApiKeyAuthentication()
        if apikey_auth.is_authenticated(request) == True:
            user_provider_tokens = SocialToken.objects.filter(user=request.user, app__provider=provider)
            if user_provider_tokens:
                user_provider_tokens.delete()

            response_data = {'status': "success"}

            return HttpResponse(json.dumps(response_data), mimetype='application/json')

    def change_password(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        apikey_auth = ApiKeyAuthentication()
        if apikey_auth.is_authenticated(request) == True:
            data = self.deserialize(request, request.body,
                                    format=request.META.get('CONTENT_TYPE', 'application/json'))
            if request.user.has_usable_password():
                password_change_form = ChangePasswordForm(request.user, data)
            else:
                password_change_form = SetPasswordForm(request.user, data)

            if password_change_form.is_valid():
                password_change_form.save()
                response_data = {'status': "success"}
                if request.user.is_authenticated():
                    logout(request)
            else:
                if request.user.is_authenticated():
                    logout(request)
                return self.create_response(request, {
                    'error': password_change_form.errors,
                }, HttpBadRequest)

            return HttpResponse(json.dumps(response_data), mimetype='application/json')

    def reset_password(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))
        try:
            email = data.get('email')
            user = User.objects.get(email=email)
            send_reset_password_email(user, request)
            response_data = {'status': 'success'}
            return HttpResponse(json.dumps(response_data), mimetype='application/json')
        except Exception as e:
            return self.create_response(request, {
                'error': e.message,
            }, HttpBadRequest)

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))

        username_or_email = data.get('username_or_email', '')
        password = data.get('password', '')

        user, error = check_user(username_or_email, password)

        if user:
            check_user_profile(user)
            return self.generate_response(request, user)
        return self.create_response(request, {
            'error': error,
        }, HttpUnauthorized)

    def avatar_upload(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if 'multipart/form-data' not in str(request.META['CONTENT_TYPE']):
            return self.create_response(request, {
                'error': 'Unsupported media type',
            }, HttpBadRequest)
        else:
            if ('photo' in request.FILES):
                avatar_photo = AvatarPhoto(photo=request.FILES['photo'])
                avatar_photo.save()

                apikey_auth = ApiKeyAuthentication()
                if apikey_auth.is_authenticated(request) == True:
                    profile = check_user_profile(request.user)
                    profile.update_avatar(avatar_url=avatar_photo.photo.url, force=True)

                return self.create_response(
                    request,
                    {'url': avatar_photo.photo.url})
            else:
                return self.create_response(request, {
                    'error': 'No image found',
                }, HttpBadRequest)

    def get_request_data(self, request, provider):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))
        access_token = data.get('access_token', '')
        refresh_token = data.get('refresh_token', '')
        device_token = data.get('device_token', None)

        if refresh_token == '' and provider == FACEBOOK:
            refresh_token = access_token

        return access_token, refresh_token, device_token

    def generate_response(self, request, user):
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        bundle = self.build_bundle(obj=user, request=request)
        bundle = self.full_dehydrate(bundle)
        apikey = ApiKey.objects.get_or_create(user=user)[0].key
        bundle.data['apikey'] = apikey
        social_access_token = SocialToken.get_user_tokens(user)
        if social_access_token:
            bundle.data['social_access_token'] = social_access_token
        return self.create_response(request, bundle)

    def google_login(self, request, **kwargs):
        access_token, refresh_token, device_token = self.get_request_data(request, GOOGLE)
        google = SocialApp.objects.get(provider=GOOGLE)
        google_adapter = GoogleAdapter(app=google, login_url='https://www.googleapis.com/oauth2/v1/userinfo',
                                       access_token=access_token, refresh_token=refresh_token)
        try:
            user = google_adapter.get_user()
            profile = check_user_profile(user)

            # Update avatar from google
            google_avatar = google_adapter.token.extra_data.get('picture', None)
            if google_avatar:
                profile.update_avatar(google_avatar)

            # If login with google then clear email confirmations
            EmailConfirmation.clear_email_confirmations(user)

            return self.generate_response(request, user)
        except Exception as e:
            return self.create_response(request, {
                'error': e.message,
            }, HttpBadRequest)

    def facebook_login(self, request, **kwargs):
        access_token, refresh_token, device_token = self.get_request_data(request, FACEBOOK)
        facebook = SocialApp.objects.get(provider=FACEBOOK)
        facebook_adapter = FacebookAdapter(app=facebook, login_url='https://graph.facebook.com/me',
                                           access_token=access_token, refresh_token=refresh_token)
        try:
            user = facebook_adapter.get_user()
            profile = check_user_profile(user)
            # Save facebook username into profile for special usage
            # Since the facebook graph api cannot get email
            # So we can use facebook username to check contact later
            token = facebook_adapter.token
            facebook_username = token.extra_data.get('username', None)
            if facebook_username:
                profile.facebook_username = facebook_username
                profile.save()

            # Update avatar from facebook
            facebook_uid = token.extra_data.get('id', None)
            facebook_avatar = None
            if facebook_uid:
                facebook_avatar = "http://graph.facebook.com/%s/picture?type=large" % facebook_uid
            if facebook_avatar:
                profile.update_avatar(facebook_avatar)

            # If login with google then clear email confirmations
            EmailConfirmation.clear_email_confirmations(user)

            return self.generate_response(request, user)
        except Exception as e:
            return self.create_response(request, {
                'error': e.message,
            }, HttpBadRequest)


class CreateUserResource(MyBaseResource):
    class Meta:
        detail_allowed_methods = []
        list_allowed_methods = ['post']
        queryset = User.objects.all()
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        try:
            email = bundle.data.get('email', None)
            username = bundle.data.get('username', None)
            password = bundle.data.get('password', None)
            if username == None:
                kwargs['username'] = email

            if email == None or password == None:
                raise BadRequest('email and password are required.')

            if User.objects.filter(email=email).count() > 0:
                raise BadRequest('A user is already registered with this e-mail address.')

            bundle = super(CreateUserResource, self).obj_create(bundle, **kwargs)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save()

            ec = EmailConfirmation.create(email)
            if ec:
                ec.send(bundle.request, signup=True)

            device_token = bundle.data.get('device_token', None)
            handle_user_profile(bundle.obj, bundle.data)

            return bundle
        except Exception as e:
            raise BadRequest(e)

    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))

        user_resource = UserResource()
        updated_bundle = user_resource.build_bundle(obj=updated_bundle.obj, request=request)
        updated_bundle = user_resource.full_dehydrate(updated_bundle)
        apikey = ApiKey.objects.get_or_create(user=updated_bundle.obj)[0].key
        updated_bundle.data['apikey'] = apikey
        location = user_resource.get_resource_uri(updated_bundle)

        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)
