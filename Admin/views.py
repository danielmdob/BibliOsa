from django.db import IntegrityError
from pip._vendor.distro import name

from SoftwareBiblio.models import Book, Author, UnregisteredUser, Administrator, Genre, RegisteredUser, Loan
from SoftwareBiblio.utils import rest_utils
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from RegisteredUser import utils
from Admin.services import category_service, book_service, author_service
from RegisteredUser.serializers import book_serializer, user_serializer, loan_serializer

import isbnlib

'''This file holds all the possible views for an administrator user. There is a user validation, if its an admin
the system must render the template, of not gives a 403:Forbidden HTTP response.'''

web_app_url = 'http://localhost:3000/'


# admin dashboard view. It queries the DB for loans in return date order.
# the following is the data structure sent to the template:
@login_required
def admin_dashboard(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return HttpResponseRedirect(web_app_url)
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_g_management(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin_g_management.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
@csrf_exempt
def create_category(request):
    if not utils.validate_admin(request.user):
        return HttpResponseForbidden()

    category_name = request.POST.get('name')
    if not category_name or category_name == '':
        return HttpResponseBadRequest()

    if category_service.category_already_exists(category_name):
        return HttpResponse(status=409) # conflict

    category = Genre(name=category_name)
    category.save()
    return HttpResponse()


@login_required
@csrf_exempt
def delete_category(request):
    if not utils.validate_admin(request.user):
        return HttpResponseForbidden()

    category_id = request.POST.get('id')

    if not category_id or category_id == '':
        return HttpResponseBadRequest()

    try:
        category = Genre.objects.get(id=category_id)
        category.delete()
        return HttpResponse()
    except Genre.DoesNotExist:
        return HttpResponseNotFound()


@login_required
@csrf_exempt
def edit_category(request):
    if not utils.validate_admin(request.user):
        return HttpResponseForbidden()

    category_id = request.POST.get('id')
    new_name = request.POST.get('name')

    if not category_id or category_id == '' or not new_name or new_name == '':
        return HttpResponseBadRequest()

    if category_service.category_already_exists(new_name):
        return HttpResponse(status=409)

    try:
        category = Genre.objects.get(id=category_id)
        category.name = new_name
        category.save()
        return HttpResponse()
    except Genre.DoesNotExist:
        return HttpResponseNotFound()


@login_required
@csrf_exempt
def add_book(request):
    if not utils.validate_admin(request.user):
        return HttpResponseForbidden()

    title = rest_utils.get_post_param(request, 'title')
    authors = request.POST.get("authors").split(',')
    isbn10 = rest_utils.get_post_param(request, 'isbn10')
    isbn13 = rest_utils.get_post_param(request, 'isbn13')
    issn = rest_utils.get_post_param(request, 'issn')
    call_number = rest_utils.get_post_param(request, 'call_number')
    publisher = rest_utils.get_post_param(request, 'publisher')
    edition = rest_utils.get_post_param(request, 'edition')
    year = rest_utils.get_post_param(request, 'year')
    copies = rest_utils.get_post_param(request, 'copies')
    book_cover_url = rest_utils.get_post_param(request, 'book_cover_url')
    category_id = rest_utils.get_post_param(request, 'category_id')

    if not title or title == '' or not copies or copies == '':
        return HttpResponseBadRequest()

    if isbn10 is not None:
        preexisting_book = book_service.get_book_by_isbn10(isbn10)
        if preexisting_book is not None:
            return JsonResponse(book_serializer.get_book_add_error_serializer(preexisting_book, 'isbn10'), status=409)

    if isbn13 is not None:
        preexisting_book = book_service.get_book_by_isbn13(isbn13)
        if preexisting_book is not None:
            return JsonResponse(book_serializer.get_book_add_error_serializer(preexisting_book, 'isbn13'), status=409)

    if call_number is not None:
        preexisting_book = book_service.get_book_by_call_number(call_number)
        if preexisting_book is not None:
            return JsonResponse(book_serializer.get_book_add_error_serializer(preexisting_book, 'call_number'), status=409)

    if category_id is not None:
        try:
            Genre.objects.get(id=category_id)
        except Genre.DoesNotExist:
            return HttpResponseNotFound()

    book = Book(title=title, isbn10=isbn10, isbn13=isbn13, issn=issn, call_number=call_number, publisher=publisher,
                edition=edition, year=year, copies=copies, cover=book_cover_url, genre_id=category_id)
    book.save()
    author_service.handle_authors_in_book_add(authors, book)
    return HttpResponse()


@login_required
@csrf_exempt
def edit_book(request):
    if not utils.validate_admin(request.user):
        return HttpResponseForbidden()

    book_id = rest_utils.get_post_param(request, 'id')
    title = rest_utils.get_post_param(request, 'title')
    authors = request.POST.get("authors").split(',')
    isbn10 = rest_utils.get_post_param(request, 'isbn10')
    isbn13 = rest_utils.get_post_param(request, 'isbn13')
    issn = rest_utils.get_post_param(request, 'issn')
    call_number = rest_utils.get_post_param(request, 'call_number')
    publisher = rest_utils.get_post_param(request, 'publisher')
    edition = rest_utils.get_post_param(request, 'edition')
    year = rest_utils.get_post_param(request, 'year')
    copies = rest_utils.get_post_param(request, 'copies')
    book_cover_url = rest_utils.get_post_param(request, 'book_cover_url')
    category_id = rest_utils.get_post_param(request, 'category_id')

    if not book_id or book_id == '' or not book_id.isdigit():
        return HttpResponseBadRequest()

    book_id = int(book_id)

    if not title or title == '' or not copies or copies == '':
        return HttpResponseBadRequest()

    try:
        saved_book = Book.objects.get(id=book_id)
        created = saved_book.created
    except Book.DoesNotExist:
        return HttpResponseNotFound()

    if isbn10 is not None:
        preexisting_book = book_service.get_book_by_isbn10(isbn10)
        if preexisting_book is not None and preexisting_book.id != book_id:
            return JsonResponse(book_serializer.get_book_add_error_serializer(preexisting_book, 'isbn10'), status=409)

    if isbn13 is not None:
        preexisting_book = book_service.get_book_by_isbn13(isbn13)
        if preexisting_book is not None and preexisting_book.id != book_id:
            return JsonResponse(book_serializer.get_book_add_error_serializer(preexisting_book, 'isbn13'), status=409)

    if call_number is not None:
        preexisting_book = book_service.get_book_by_call_number(call_number)
        if preexisting_book is not None and preexisting_book.id != book_id:
            return JsonResponse(book_serializer.get_book_add_error_serializer(preexisting_book, 'call_number'), status=409)

    if category_id is not None:
        try:
            Genre.objects.get(id=category_id)
        except Genre.DoesNotExist:
            return HttpResponseNotFound()

    book = Book(id=book_id, title=title, isbn10=isbn10, isbn13=isbn13, issn=issn, call_number=call_number, publisher=publisher,
                edition=edition, year=year, copies=copies, cover=book_cover_url, genre_id=category_id, created=created)
    book.save()
    book.authors.clear()
    author_service.handle_authors_in_book_add(authors, book)
    return HttpResponse()


@login_required
@csrf_exempt
def delete_book(request):
    if not utils.validate_admin(request.user):
        return HttpResponseForbidden()

    book_id = rest_utils.get_post_param(request, 'id')
    if not book_id or book_id == '' or not book_id.isdigit():
        return HttpResponseBadRequest()

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponseNotFound()

    authors = book.authors.all()
    author_service.handle_authors_in_book_delete(authors)

    book.delete()
    return HttpResponse()


@login_required
@csrf_exempt
def subscribe_user(request):
    if not utils.validate_admin(request.user):
        return HttpResponseForbidden()

    email = rest_utils.get_post_param(request, 'email')
    first_name = rest_utils.get_post_param(request, 'first_name')
    last_name = rest_utils.get_post_param(request, 'last_name')
    card_number = rest_utils.get_post_param(request, 'card_number')

    if (first_name is None or first_name.isspace()) or (last_name is None or last_name.isspace()) or (card_number is None or card_number.isspace()):
        return HttpResponseBadRequest()

    registered_user = RegisteredUser(email=email, first_name=first_name, last_name=last_name, card_number=card_number)
    try:
        registered_user.save()
        serialized_user = user_serializer.user_serializer(registered_user)
    except IntegrityError:
        try:
            conflicting_user = RegisteredUser.objects.get(card_number=card_number)
            return JsonResponse(user_serializer.user_serializer(conflicting_user), status=409)
        except RegisteredUser.DoesNotExist:
            conflicting_user = RegisteredUser.objects.get(email=email)
            return JsonResponse(user_serializer.user_serializer(conflicting_user), status=409)

    return JsonResponse(serialized_user)


@login_required
def search_user_by_name(request):
    if not utils.validate_admin(request.user):
        return HttpResponseForbidden()

    search_string = request.GET.get('search_string')

    if not search_string or search_string.isspace():
        return HttpResponseBadRequest()

    found_users = RegisteredUser.objects.filter(first_name__icontains=search_string)
    return JsonResponse(user_serializer.user_list_serializer(found_users), safe=False)


@login_required
@csrf_exempt
def loan_book(request):
    if not utils.validate_admin(request.user):
        return HttpResponseForbidden()

    reader_id = rest_utils.get_post_param(request, 'reader_id')
    return_date = rest_utils.get_post_param(request, 'return_date')
    book_id = rest_utils.get_post_param(request, 'book_id')

    if (reader_id is None or reader_id.isspace() or not reader_id.isdigit()) or (return_date is None or return_date.isspace()) or (book_id is None or book_id.isspace() or not book_id.isdigit()):
        return HttpResponseBadRequest()

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponseNotFound()

    if len(book.loan_set.all()) >= book.copies:
        return HttpResponseBadRequest()

    loan = Loan(reader_id=reader_id, return_date=return_date, is_active=True, book_id=book_id)
    loan.save()

    return HttpResponse()


def get_book_loans(request):
    if not utils.validate_admin(request.user):
        return HttpResponseForbidden()

    book_id = request.GET.get('book_id')

    if book_id is None or book_id.isspace() or not book_id.isdigit():
        return HttpResponseBadRequest()

    loans = Loan.objects.filter(book_id=book_id, is_active=True)

    return JsonResponse(loan_serializer.serialize_loans(loans), safe=False)
