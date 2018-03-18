from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User, Permission
from SoftwareBiblio.models import UnregisteredUser, RegisteredUser, Administrator
from django.contrib.auth.views import login


def home(request):
    return render(request, '../templates/Admin/home.html')


def register(request):
    return render(request, '../templates/registration/register.html')


def permission_denied(request):
    return HttpResponseForbidden()


@login_required
def reader_dashboard(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-dashboard.html')


def chose_login(request):
    logged_user = request.user
    email = logged_user.email
    try: #este caso nunca va a pasar pero es necesario para no hacer 1000 de estas adentro
        user = User.objects.get(email=email)
        try:
            admin = Administrator.objects.get(user=user)
            return HttpResponseRedirect('admin_dashboard')
        except Administrator.DoesNotExist:
            try:
                unregisteredUser = UnregisteredUser.objects.get(email=email)
                try:
                    registeredUser = RegisteredUser.objects.get(user=user)
                    RegisteredUser.objects.filter(user=user).delete()
                    admin = Administrator(user=registeredUser.user, cedula=registeredUser.cedula,
                                          address=registeredUser.address, city=registeredUser.city,
                                          phone=registeredUser.phone)
                    admin.save()
                    return HttpResponseRedirect('admin_dashboard')
                except RegisteredUser.DoesNotExist:
                    return HttpResponseRedirect('register')
            except UnregisteredUser.DoesNotExist:
                try:
                    registeredUser = RegisteredUser.objects.get(user=user)
                    return HttpResponseRedirect('reader_dashboard')
                except RegisteredUser.DoesNotExist:
                    return HttpResponseRedirect('register')
    except User.DoesNotExist:
        return HttpResponseRedirect('register')


def finish_register(request):
    cedula = request.GET.get('cedula', None)
    email = request.GET.get('email', None)
    address = request.GET.get('address', None)
    city = request.GET.get('city', None)
    phone = request.GET.get('phone', None)
    # print("%s %s %s %s %s %s" % (fullname, cedula, email, address, city, phone))
    # hacer el registro a la base de datos
    print(email)
    try:
        print(email)
        user = UnregisteredUser.objects.get(email=email)
        dashboard = 1  # admin dashboard
        admin = Administrator(user=User.objects.get(email=email), cedula=cedula, address=address,
                              city=city, phone=phone)
        admin.save()
    except UnregisteredUser.DoesNotExist:
        dashboard = 0  # reader dashboard
        registered_user = RegisteredUser(user=User.objects.get(email=email), cedula=cedula,
                                         address=address, city=city,
                                         phone=phone)
        registered_user.save()
    data = {'dashboard': dashboard}
    return JsonResponse(data)


@login_required
def reader_about(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-about.html')


@login_required
def reader_book(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-book.html')


@login_required
def reader_contact_admins(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-contactAdmins.html')


@login_required
def reader_contact_developers(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-contactDevelopers.html')


@login_required
def reader_edit_my_profile(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-editMyProfile.html')


@login_required
def reader_genre(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-genre.html')


@login_required
def reader_loan_page(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-loanPage.html')


@login_required
def reader_my_profile(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-myProfile.html')


@login_required
def reader_search_results(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-searchResults.html')


@login_required
def reader_terms_of_use(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-termsOfUse.html')


@login_required
def reader_view_loans(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-viewLoans.html')


@login_required
def reader_books(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-books.html')


@login_required
def reader_genres(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        return render(request, '../templates/RegisteredUser/reader-genres.html')
