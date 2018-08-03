from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User, Permission
from django.views.decorators.csrf import csrf_exempt

from SoftwareBiblio.models import UnregisteredUser, RegisteredUser, Administrator, Loan, Copy, Book, Genre
from django.contrib.auth.views import login
from urllib.request import urlopen
from RegisteredUser import utils
from RegisteredUser.services import user_service, administrator_service
from RegisteredUser.serializers import category_serializer, book_serializer

'''This file holds all the possible views for a reader user. There is a user validation, if its an admin
the system must give a 403:Forbidden HTTP response, if not the system must render the template.'''

web_app_url = 'http://localhost:3000/'

def home(request):
    return render(request, '../templates/Admin/home.html')


def register(request):
    return render(request, '../templates/registration/register.html')


def permission_denied(request):
    return HttpResponseForbidden()

# login dashboard view. It queries the DB for reader loans in return date order.
# the following is the data structure sent to the template:
# Loans([Loan_info([[return_date, Books([Book_info([title,href]),..]), Authors([normalized_name,..])]),..])
@login_required
def reader_dashboard(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseForbidden()
    except Administrator.DoesNotExist:
        registered_user = RegisteredUser.objects.get(user=User.objects.get(email=email))

        return render(request, '../templates/RegisteredUser/reader-dashboard.html', {'loans': 1})


# this view handles the authentication process, rendering the correct view for the user.
def chose_login(request):
    logged_user = request.user
    email = logged_user.email
    try:
        user = User.objects.get(email=email)
        try:
            admin = Administrator.objects.get(user=user)
            return HttpResponseRedirect(web_app_url)
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
                    return HttpResponseRedirect(web_app_url)
                except RegisteredUser.DoesNotExist:
                    return HttpResponseRedirect('register')
            except UnregisteredUser.DoesNotExist:
                try:
                    registeredUser = RegisteredUser.objects.get(user=user)
                    return HttpResponseRedirect(web_app_url)
                except RegisteredUser.DoesNotExist:
                    return HttpResponseRedirect('register')
    except User.DoesNotExist:
        return HttpResponseRedirect('register')


# register a new user
def finish_register(request):
    cedula = request.GET.get('cedula', None)
    email = request.GET.get('email', None)
    address = request.GET.get('address', None)
    city = request.GET.get('city', None)
    phone = request.GET.get('phone', None)
    # print("%s %s %s %s %s %s" % (fullname, cedula, email, address, city, phone))
    # hacer el registro a la base de datos
    try:
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
    return HttpResponse(status=200)


def is_logged_in(request):
    if request.user.is_authenticated:
        return HttpResponse("true")
    else:
        return HttpResponse("false")


def redirect_to_app(request):
    return HttpResponseRedirect(web_app_url)

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
def is_administrator(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponse("true")
    except Administrator.DoesNotExist:
        return HttpResponse("false")


@login_required
def get_user_info(request):
    user = request.user
    user_info = {
        'email' : user.email,
        'firstName' : user.first_name,
        'lastName' : user.last_name,
    }
    return JsonResponse(user_info)


@login_required
@csrf_exempt
def invite_administrator(request):
    if not utils.validate_admin(request.user):
        return HttpResponseForbidden()

    invitee_email = request.POST.get('invitee_email')
    if not invitee_email:
        return HttpResponseBadRequest()

    invitee_email = request.POST.get('invitee_email')
    if not invitee_email or invitee_email == '':
        return HttpResponseBadRequest()

    registered_user = user_service.get_user_by_email(invitee_email)
    if not registered_user:
        return HttpResponseNotFound()

    if administrator_service.is_admin(invitee_email):
        return HttpResponse(status=409)  # 409 is the status code for conflict

    registered_user.__class__ = Administrator
    registered_user.registereduser_ptr=registered_user
    registered_user.save()
    return HttpResponse()


def get_categories(request):
    categories = Genre.objects.all()
    serialized_categories = category_serializer.get_categories(categories)
    return JsonResponse(serialized_categories, safe=False)


def get_book_info(request):
    book_id = request.GET.get('id')

    if not book_id or book_id == '':
        return HttpResponseBadRequest()

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponseNotFound()

    serialized_book = book_serializer.get_basic_book_serializer(book)

    return JsonResponse(serialized_book, safe=False)