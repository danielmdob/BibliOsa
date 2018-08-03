from SoftwareBiblio.models import UnregisteredUser, RegisteredUser, Administrator, Loan, Copy, Book
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, Permission


def validate_admin(user):
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=user.email))
        return True
    except Administrator.DoesNotExist:
        return False
