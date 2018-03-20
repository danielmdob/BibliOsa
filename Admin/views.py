from SoftwareBiblio.models import Book, Author, UnregisteredUser, RegisteredUser, Administrator, BookCover, Loan, Copy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from SoftwareBiblio.forms import ImageForm
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
import isbnlib

'''This file holds all the possible views for an administrator user. There is a user validation, if its an admin
the system must render the template, of not gives a 403:Forbidden HTTP response.'''


# This view saves a book cover, it could be used as well for profile pictures. Pictures are saved under /media/documents
def admin_save_book_cover(request):
    saved = False
    if request.method == "POST":
        # Get the posted form
        my_photo_form = ImageForm(request.POST, request.FILES)
        if my_photo_form.is_valid():
            image = BookCover()
            image.image = my_photo_form.cleaned_data["picture"]
            book_isbn = my_photo_form.cleaned_data["book_isbn"]
            image.save()  # create and save image instance
            book = Book.objects.get(ISBN=book_isbn)
            book.cover = image
            book.save()  # update book instance with the new cover
            saved = True
    else:
        MyImageForm = ImageForm()

    return render(request, '../templates/Admin/admin-editBook.html', locals())

# This view sends an email invitation for a user.
def admin_send_invite(request):
    email = request.GET.get('email', None)
    try: # if email already got an invitation do not send it
        user = UnregisteredUser.objects.get(email=email)
        response = "Ya se ha enviado una invitación a esta dirección antes."
        data = {'response': response}
        return JsonResponse(data)
    except UnregisteredUser.DoesNotExist:
        try:
            user = User.objects.get(email=email)
            try: # si ya es admin para que..
                user = Administrator.objects.get(user=user) # if user is already an admin do not send the invite
                response = "Esta dirección corresponde a un administrador."
                data = {'response': response}
                return JsonResponse(data)
            except Administrator.DoesNotExist: # send it if its a reader.
                response = "Se ha enviado una invitación a " + email
                data = {'response': response}
                unregisteredUser = UnregisteredUser(email=email)
                unregisteredUser.save()
                mail = EmailMessage('Invitación para ser administrador de BibliOsa',
                                    'Usted ha sido invitado como administrador'
                                    'de BibliOsa, por favor siga este enlace y proceda a entrar con'
                                    ' sus credenciales de Google:\n127.0.0.1:8000'
                                    '', to=[email])
                mail.send()
                return JsonResponse(data)
        except User.DoesNotExist: # send it for new user
            response = "Se ha enviado una invitación a " + email
            data = {'response': response}
            unregisteredUser = UnregisteredUser(email=email)
            unregisteredUser.save()
            mail = EmailMessage('Invitación para ser administrador de BibliOsa',
                                'Usted ha sido invitado como administrador'
                                'de BibliOsa, por favor siga este enlace'
                                'y proceda a entrar con sus credenciales '
                                'de Google:\n127.0.0.1:8000'
                                '', to=[email])
            mail.send()
            return JsonResponse(data)


# admin dashboard view. It queries the DB for loans in return date order.
# the following is the data structure sent to the template:
# Loans([Loan_info([[return_date, Books([Book_info([title,href]),..]), Authors([normalized_name,..]),reader_name,reader_href]),..])
@login_required
def admin_dashboard(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        loan_set = Loan.objects.all().order_by('return_date')
        loans = []
        loans_counter = 0
        for loan in loan_set:
            loan_info = []
            return_date = loan.return_date
            # print(return_date)
            loan_info.insert(0, return_date)
            loan_copy_set = Copy.objects.filter(loan_id=loan.id)
            books = []
            book_counter = 0
            for copy in loan_copy_set:
                book = Book.objects.filter(id=copy.book_id)
                for b in book:
                    book_title = b.title
                    # print(book_title)
                    book_href = "admin_book?id=" + str(b.id)
                    # print(book_href)
                    book_info = []
                    book_info.insert(0, book_title)
                    book_info.insert(1, book_href)
                    books.insert(book_counter, book_info)
                    authors = []
                    author_set = b.authors.all()
                    author_counter = 0
                    for author in author_set:
                        authors.insert(author_counter, author.normalized_name)
                        author_counter += 1
                        # print(authors)
            loan_info.insert(1, books)
            loan_info.insert(2, authors)
            reader = RegisteredUser.objects.filter(id=loan.reader_id)
            for r in reader: # even if its one user it was giving error, so I made a for for 1 element to solve it...
                reader_name = r.user.first_name + " " + r.user.last_name
                # print(reader_name)
                reader_href = "admin_reader_profile?id=" + str(r.id)
                # print(reader_href)
                loan_info.insert(3, reader_name)
                loan_info.insert(4, reader_href)
            loans.insert(loans_counter, loan_info)
            loans_counter += 1
        print(loans)
        return render(request, '../templates/Admin/admin-dashboard.html', {'loans': loans})
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_profile(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-profile.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_about(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-about.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_add_device(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-addDevice.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_admin_search(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-adminSearch.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_book(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-book.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_contact_admins(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-contactAdmins.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_contact_developers(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-contactDevelopers.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_devices(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-Devices.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_edit_admin_profile(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-editAdminProfile.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_edit_book(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-editBook.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_edit_my_profile(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-editMyProfile.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_edit_reader_profile(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-editReaderProfile.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_genre(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-genre.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_invite_admin(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-inviteAdmin.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_loan_page(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-loanPage.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_make_loan(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-makeLoan.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_manual_add(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-manualAdd.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_my_profile(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-myProfile.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_reader_profile(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-readerProfile.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_reader_search(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-readerSearch.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_search_results(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-readerSearchResults.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_terms_of_use(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-termsOfUse.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def admin_view_loans(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-viewLoans.html')
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
def admin_user_search(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-userSearch.html')
    except Administrator.DoesNotExist:
        return HttpResponseForbidden()


@login_required
def book_management(request):
    user = request.user
    email = user.email
    try:
        admin = Administrator.objects.get(user=User.objects.get(email=email))
        return render(request, '../templates/Admin/admin-bookManagement.html')
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
                handleAuthors(book, bookInfo['Authors'])

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
        except TypeError:
            data = {
                'is_valid': False
            }

    return JsonResponse(data)


def handleAuthors(book, authors):
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


'''def addBookCover(url, book):
    bookCover = BookCover()
    save_image_from_url(BookCover.image, url)
    book.save()

def save_image_from_url(field, url):
    bookCover = BookCover()
    bookCover.url = url
    bookCover.save()
    bookCover.get_remote_image()'''
