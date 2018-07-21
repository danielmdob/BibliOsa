from pip._vendor.distro import name

from SoftwareBiblio.models import Book, Author, UnregisteredUser, Administrator, BookCover, Genre
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from SoftwareBiblio.forms import ImageForm
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from RegisteredUser import utils
from Admin.services import category_service

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

'''def addBookCover(url, book):
    bookCover = BookCover()
    save_image_from_url(BookCover.image, url)
    book.save()

def save_image_from_url(field, url):
    bookCover = BookCover()
    bookCover.url = url
    bookCover.save()
    bookCover.get_remote_image()'''
