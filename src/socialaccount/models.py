import datetime
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.timezone import get_current_timezone, make_aware
from django.utils.translation import gettext_lazy as _

from jsonfield import JSONField
from model_utils.models import TimeStampedModel
from encrypted_fields import EncryptedTextField

from commons import generate_key


GOOGLE = 'google'
FACEBOOK = 'facebook'


SOCIAL_APP_CHOICES = (
    ('facebook', _(u'Facebook')),
    ('google', _(u'Google')),
)


@python_2_unicode_compatible
class SocialApp(models.Model):
    provider = models.CharField(max_length=30,
                                choices=SOCIAL_APP_CHOICES, unique=True)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=100,
                                 help_text='App ID, or consumer key')
    key = models.CharField(max_length=100,
                           blank=True,
                           help_text='Key (Stack Exchange only)')
    secret = models.CharField(max_length=100,
                              help_text='API secret, client secret, or'
                              ' consumer secret')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class SocialToken(TimeStampedModel):
    app = models.ForeignKey(SocialApp)
    user = models.ForeignKey(User)
    token = EncryptedTextField(help_text='"oauth_token" (OAuth1) or access token (OAuth2)')
    token_secret = EncryptedTextField(blank=True,
                   help_text='"oauth_token_secret" (OAuth1) or refresh'
                             ' token (OAuth2)')
    expires = models.PositiveIntegerField(null=True, blank=True)
    extra_data = JSONField(default='{}')

    class Meta:
        unique_together = ('app', 'user')

    def __str__(self):
        return self.token

    @property
    def almost_expired(self):
        '''
        Used this method to check if the token will be expired in 5 minutes
        Then we need to refresh this token
        :return:
        '''
        if self.expires == None:
            return True
        now = datetime.datetime.utcnow()
        modified = self.modified.replace(tzinfo=None)
        if (now-modified).seconds > self.expires - 300:
            return True
        return False

    @property
    def json(self):
        return {
            self.app.provider: {
                'token': self.token
            }
        }

    @classmethod
    def get_user_tokens(cls, user):
        social_tokens = SocialToken.objects.filter(user=user)
        result = {}
        for t in social_tokens:
            result.update(t.json)

        return result
