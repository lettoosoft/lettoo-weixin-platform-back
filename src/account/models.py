import datetime

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from .signals import password_reset
from .utils import random_token, send_mail


EMAIL_CONFIRMATION_EXPIRE_DAYS = 3


class EmailConfirmationManager(models.Manager):
    def all_expired(self):
        return self.filter(self.expired_q())

    def all_valid(self):
        return self.exclude(self.expired_q())

    def expired_q(self):
        sent_threshold = timezone.now() \
                         - datetime.timedelta(days=EMAIL_CONFIRMATION_EXPIRE_DAYS)
        return Q(sent__lt=sent_threshold)

    def delete_expired_confirmations(self):
        self.all_expired().delete()


@python_2_unicode_compatible
class EmailConfirmation(TimeStampedModel):
    user = models.ForeignKey(User)
    email = models.EmailField(unique=True, verbose_name=_('e-mail address'))
    sent = models.DateTimeField(verbose_name=_('sent'), null=True)
    key = models.CharField(verbose_name=_('key'), max_length=64, unique=True)
    verified = models.BooleanField(verbose_name=_('verified'), default=False)
    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _('email confirmation')
        verbose_name_plural = _('email confirmations')

    def __str__(self):
        return u'confirmation for %s' % self.email

    @classmethod
    def create(cls, email):
        try:
            user = User.objects.get(email=email)
            key = random_token([email])
            return cls._default_manager.create(user=user, email=email, key=key)
        except User.DoesNotExist:
            return None

    def key_expired(self):
        expiration_date = self.sent \
                          + datetime.timedelta(days=EMAIL_CONFIRMATION_EXPIRE_DAYS)
        return expiration_date <= timezone.now()

    key_expired.boolean = True

    def confirm(self, request):
        if not self.key_expired() and not self.verified:
            self.verified = True
            self.save()

    def send(self, request, signup=False, **kwargs):
        activate_url = reverse('account_confirm_email', args=[self.key])
        activate_url = request.build_absolute_uri(activate_url)
        ctx = {
            'activate_url': activate_url,
        }
        email_template = 'email/signup_with_email.html'
        current_site = Site.objects.get_current()
        subject = 'Reset password'
        send_mail(email_template,
                  subject,
                  self.email,
                  ctx)
        self.sent = timezone.now()
        self.save()

    @classmethod
    def clear_email_confirmations(cls, user):
        email_confirmations = cls.objects.filter(user=user)
        email_confirmations.delete()


def send_password_changed_email(sender, request, user, **kwargs):
    send_mail(
        email_template='account/email/password_changed.html',
        subject='Your password has been changed',
        to_email=user.email,
        ctx={})


password_reset.connect(send_password_changed_email, dispatch_uid='send_password_changed_email')
