import urllib2
from urlparse import parse_qs

import requests
from django.contrib.auth.models import User

from socialaccount.models import SocialToken


class SocialAdapter(object):
    def __init__(self, app, access_token, refresh_token, login_url=None):
        self.app = app
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.login_url = login_url
        self.email = None
        self.error = None


    def social_login(self):
        try:
            resp = requests.get(self.login_url,
                                params={'access_token': self.access_token, 'alt': 'json'})
            if resp.status_code == 200:
                self.extra_data = resp.json()
            else:
                self.error = resp.reason
        except Exception as e:
            self.error = e.message

    def check_valid_email(self):
        raise NotImplementedError('Not Implemented')


    def get_user_data(self):
        raise NotImplementedError('Not Implemented')

    def get_or_create_token(self, user):
        token = SocialToken.objects.get_or_create(app=self.app, user=user)[0]
        token.token = self.access_token
        token.token_secret = self.refresh_token
        token.extra_data = self.extra_data
        token.save()
        self.token = token

    def get_user(self):
        self.social_login()
        if self.error:
            raise Exception(self.error)
        if not self.check_valid_email():
            raise Exception('The email did not valid')
        user = self.get_user_data()
        self.get_or_create_token(user)
        return user

    def refresh_access_token(self, social_token):
        raise NotImplementedError('Not Implemented')


class GoogleAdapter(SocialAdapter):
    def check_valid_email(self):
        if self.extra_data.get('email', None) and self.extra_data.get('verified_email'):
            self.email = self.extra_data.get('email', None)
            return True
        return False

    def get_user_data(self):
        first_name = self.extra_data.get('given_name', '')
        last_name = self.extra_data.get('family_name', '')
        user, created = User.objects.get_or_create(email=self.email)
        if created:
            user.username = self.email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user

    def refresh_access_token(self, social_token):
        #https://developers.google.com/accounts/docs/OAuth2WebServer#offline
        url = 'https://accounts.google.com/o/oauth2/token'
        data = {
            'client_id': self.app.client_id,
            'client_secret': self.app.secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        resp = requests.post(url, data=data)
        if resp.status_code == 200:
            resp_data = resp.json()
            access_token = resp_data['access_token']
            expires = resp_data['expires_in']
            social_token.token = access_token
            social_token.token_secret = self.refresh_token
            social_token.expires = expires
            social_token.save()
        else:
            raise Exception(resp.reason)


class FacebookAdapter(SocialAdapter):
    def check_valid_email(self):
        if self.extra_data.get('email', None) and self.extra_data.get('verified'):
            self.email = self.extra_data.get('email', None)
            return True
        return False

    def get_user_data(self):
        username = self.extra_data.get('username')
        first_name = self.extra_data.get('first_name', '')
        last_name = self.extra_data.get('last_name', '')
        user, created = User.objects.get_or_create(email=self.email)
        if created:
            user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user

    def refresh_access_token(self, social_token):
        url = 'https://graph.facebook.com/oauth/access_token' \
                  '?client_id=%s' \
                  '&client_secret=%s' \
                  '&grant_type=fb_exchange_token' \
                  '&fb_exchange_token=%s' % (self.app.client_id, self.app.secret, self.refresh_token)
        resp = parse_qs(urllib2.urlopen(url).read())
        access_token = resp['access_token'][0]
        expires = resp['expires'][0]

        social_token.token = access_token
        social_token.token_secret = self.refresh_token
        social_token.expires = expires
        social_token.save()
        return True
