from pip._vendor.distro import name

from SoftwareBiblio.models import Book, Author, UnregisteredUser, Administrator, Genre
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from RegisteredUser import utils
from Admin.services import category_service, book_service
from RegisteredUser.serializers import book_serializer

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


def smart_add(request):
    isbn = request.GET.get('isbn', None)

    if isbnlib.notisbn(isbn):
        data = {
            'is_valid': False
        }
    else:
        bookInfo = isbnlib.meta(isbn)  # Datos que provee meta: Title Authors Publisher Language
        cover = isbnlib.cover(isbn)
        bookInfo = isbnlib.meta(isbn)  # Datos que provee meta: Title Authors Publisher Language
        try:
            alreadyAdded = False
            book = Book()
            book.title = bookInfo['Title']
            book.publisher = bookInfo['Publisher']
            book.ISBN = isbn
            if Book.objects.filter(ISBN=isbn).count() > 0:
                alreadyAdded = True
                print("repetido")
            else:
                book.save()
                handle_authors(book, bookInfo['Authors'])

            if cover:  # COMPLETAR
                print("si")
            else:
                print("no")

            data = {
                'is_valid': True,
                'already_added': alreadyAdded,
                'title': bookInfo['Title'],
                'publisher': bookInfo['Publisher'],
                'isbn': isbn,
            }
        except TypeError:
            print("Type Error")
            data = {
                'is_valid': False,
                'publisher': bookInfo['Publisher']
            }

    return JsonResponse(data)


def handle_authors(book, authors):
    for author in authors:
        dbAuthor = Author.objects.filter(fullName=author)
        if dbAuthor.count() == 0:
            newAuthor = Author()
            newAuthor.fullName = author
            newAuthor.save()
            book.authors.add(newAuthor)
            book.save()
        else:
            dbAuthor = Author.objects.get(fullName=author)
            book.authors.add(dbAuthor)
            book.save()


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

    title = request.POST.get('title')
    authors = request.POST.getlist("authors")  # it may be authors[]
    isbn10 = request.POST.get('isbn10')
    isbn13 = request.POST.get('isbn13')
    issn = request.POST.get('issn')
    call_number = request.POST.get('call_number')
    publisher = request.POST.get('publisher')
    edition = request.POST.get('edition')
    year = request.POST.get('year')
    copies = request.POST.get('copies')
    book_cover_url = request.POST.get('book_cover_url')

    if not title or title == '' or not copies or copies == '':
        return HttpResponseBadRequest()

    preexisting_book = book_service.get_book_by_isbn10(isbn10)
    if preexisting_book is not None:
        return JsonResponse(book_serializer.get_book_add_error_serializer(preexisting_book, 'isbn10'), status=409)

    preexisting_book = book_service.get_book_by_isbn13(isbn13)
    if preexisting_book is not None:
        return JsonResponse(book_serializer.get_book_add_error_serializer(preexisting_book, 'isbn13'), status=409)

    preexisting_book = book_service.get_book_by_call_number(call_number)
    if preexisting_book is not None:
        return JsonResponse(book_serializer.get_book_add_error_serializer(preexisting_book, 'call_number'), status=409)

    book = Book(title=title, isbn10=isbn10, isbn13=isbn13, issn=issn, call_number=call_number, publisher=publisher,
                edition= edition, year=year, copies=copies, cover=book_cover_url)

    return HttpResponse()

'''def addBookCover(url, book):
    bookCover = BookCover()
    save_image_from_url(BookCover.image, url)
    book.save()

def save_image_from_url(field, url):
    bookCover = BookCover()
    bookCover.url = url
    bookCover.save()
    bookCover.get_remote_image()'''
