from .models import Profile


def check_user_profile(user):
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)
        profile.save()
    return profile


def handle_user_profile(user, data):
    profile = check_user_profile(user)
    for field in user._meta.get_fields_with_model():
        data.pop(field[0].name, None)
    if profile.extra_data:
        profile.extra_data.update(data)
    else:
        profile.extra_data = data
    profile.save()
