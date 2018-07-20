from django.contrib.auth.models import User

from SoftwareBiblio.models import RegisteredUser


def get_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        registered_user = RegisteredUser.objects.get(user=user)
        return registered_user
    except User.DoesNotExist or RegisteredUser.DoesNotExist:
        return None
