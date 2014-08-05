import re
from django.contrib.auth.models import User
from tastypie.exceptions import BadRequest


def check_user(username_or_email, password):
    try:
        user = User.objects.get(username=username_or_email)
    except User.DoesNotExist:
        user = None

    if not user:
        try:
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            user = None

    error = None
    if user:
        if user.is_active:
            if not user.check_password(password):
                error = 'password is incorrect'
        else:
            error = 'user is inactive'
    else:
        error = 'no user'

    if error:
        user = None

    return user, error


def get_event_id(data):
    try:
        id_regex = re.compile("/(\d+)$")
        event_id = id_regex.findall(data)[0]
    except:
        try:
            id_regex = re.compile("/(\d+)/$")
            event_id = id_regex.findall(data)[0]
        except:
            raise BadRequest()
    return event_id