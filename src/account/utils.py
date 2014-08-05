import hashlib
import random

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36


DEFAULT_HTTP_PROTOCOL = 'http'


def random_token(extra=None, hash_func=hashlib.sha256):
    if extra is None:
        extra = []
    bits = extra + [str(random.SystemRandom().getrandbits(512))]
    return hash_func(''.join(bits).encode('utf-8')).hexdigest()


def send_reset_password_email(user, request):
    token_generator = PasswordResetTokenGenerator()

    temp_key = token_generator.make_token(user)
    # send the password reset email
    path = reverse('account_reset_password_from_key',
                   kwargs=dict(uidb36=int_to_base36(user.id),
                               key=temp_key))
    url = request.build_absolute_uri(path)
    context = {'password_reset_url': url}
    subject = '%s Reset your password' % '[Calvin]'
    send_mail('email/forget_password.html', subject, user.email, context)


def send_mail(template, subject, to_email, context):
    # TODO
    pass
