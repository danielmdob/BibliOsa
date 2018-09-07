from django.contrib.auth.models import User

from SoftwareBiblio.models import RegisteredUser


def get_user_by_email(email):
    try:
        registered_user = RegisteredUser.objects.get(email=email)
        return registered_user
    except RegisteredUser.DoesNotExist:
        return None
