from SoftwareBiblio.models import Administrator, RegisteredUser


def is_admin(email):
    try:
        user = RegisteredUser.objects.get(email=email)
        admin = Administrator.objects.get(registereduser_ptr_id=user.id)
        return True
    except RegisteredUser.DoesNotExist or Administrator.DoesNotExist:
        return False

