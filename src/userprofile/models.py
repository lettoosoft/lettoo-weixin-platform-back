from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db import models

from jsonfield import JSONField
from model_utils.models import TimeStampedModel

from commons import get_filename


class Profile(TimeStampedModel):
    user = models.OneToOneField(User)
    facebook_username = models.CharField(max_length=255, null=True, blank=True)
    extra_data = JSONField(default={}, null=True, blank=True)

    def __unicode__(self):
        return self.user.get_full_name()

    def set(self, key, value):
        self.extra_data[key] = value
        self.save()

    def get(self, key, default=None):
        value = default
        try:
            value = self.extra_data.get(key, default)
        except:
            pass

        return value

    def can_notify(self, notification_type):
        result = False
        if int(notification_type) in self.get('show_notification_types', []):
            result = True
        if str(notification_type) in self.get('show_notification_types', []):
            result = True
        return result

    def update_avatar(self, avatar_url, force=False):
        updated = False
        if force or self.get('avatar_url') == None:
            self.set('avatar_url', avatar_url)
            updated = True

        return updated


def check_userprofile(sender, request, user, **kwargs):
    try:
        profile = user.profile
    except:
        Profile(user=user).save()


user_logged_in.connect(check_userprofile)


class AvatarPhoto(TimeStampedModel):
    photo = models.ImageField(upload_to=get_filename)

    def __unicode__(self):
        return self.photo.url
