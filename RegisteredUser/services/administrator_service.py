from django.contrib.auth.models import User

from SoftwareBiblio.models import Administrator


def is_admin(email):
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return True
    except Administrator.DoesNotExist:
        return False

