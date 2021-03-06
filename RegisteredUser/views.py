from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User, Permission
from django.views.decorators.csrf import csrf_exempt

from SoftwareBiblio.models import UnregisteredUser, RegisteredUser, Administrator, Loan, Copy, Book, Genre, Author
from django.contrib.auth.views import login
from urllib.request import urlopen
from RegisteredUser import utils
from RegisteredUser.services import user_service, administrator_service
from RegisteredUser.serializers import category_serializer, book_serializer, author_serializer

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
            registered_user = RegisteredUser.objects.get(email=email)
            if registered_user.user_id is None:
                registered_user.user_id = user.id
                registered_user.save()
        except RegisteredUser.DoesNotExist:
            pass

        return HttpResponseRedirect(web_app_url)
    except User.DoesNotExist:
        return HttpResponseRedirect('register')


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
    try:
        registered_user = RegisteredUser.objects.get(email=user.email)
        user_info = {
            'email': registered_user.email,
            'firstName': registered_user.first_name,
            'lastName': registered_user.last_name,
            'isSubscribed': 'true',
        }
    except RegisteredUser.DoesNotExist:
        user_info = {
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'isSubscribed': False,
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

    if not book_id or book_id == '' or not book_id.isdigit():
        return HttpResponseBadRequest()

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponseNotFound()

    serialized_book = book_serializer.get_basic_book_serializer(book)

    return JsonResponse(serialized_book, safe=False)


def title_search_book(request):
    search_string = request.GET.get('search_string')

    if not search_string or search_string == '':
        return HttpResponseBadRequest()

    found_books = Book.objects.filter(title__icontains=search_string)
    return JsonResponse(book_serializer.search_serializer(found_books), safe=False)


def call_number_search_book(request):
    search_string = request.GET.get('search_string')

    if not search_string or search_string == '':
        return HttpResponseBadRequest()

    found_books = Book.objects.filter(call_number__istartswith=search_string)
    return JsonResponse(book_serializer.search_serializer(found_books), safe=False)


def author_search(request):
    search_string = request.GET.get('search_string')

    if not search_string or search_string == '':
        return HttpResponseBadRequest()

    found_authors = Author.objects.filter(full_name__icontains=search_string)
    return JsonResponse(author_serializer.search_serializer(found_authors), safe=False)


def get_author_info(request):
    author_id = request.GET.get('id')

    if not author_id or author_id == '':
        return HttpResponseBadRequest()

    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return HttpResponseNotFound()

    serialized_author = author_serializer.serialize_author(author)

    return JsonResponse(serialized_author, safe=False)


def get_new_arrivals(request):
    books = Book.objects.filter(created__isnull=False).order_by('-created')[:5]
    serialized_books = book_serializer.serialize_new_arrivals(books)
    return JsonResponse(serialized_books, safe=False)
