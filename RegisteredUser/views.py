from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User, Permission
from SoftwareBiblio.models import UnregisteredUser, RegisteredUser, Administrator, Loan, Copy, Book
from django.contrib.auth.views import login

'''This file holds all the possible views for a reader user. There is a user validation, if its an admin
the system must give a 403:Forbidden HTTP response, if not the system must render the template.'''


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
        loan_set = Loan.objects.filter(reader_id=registered_user.id).order_by('return_date')
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
                    book_href = "reader_book?id=" + str(b.id)
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
            loans.insert(loans_counter, loan_info)
            loans_counter += 1
        print(loans)
        return render(request, '../templates/RegisteredUser/reader-dashboard.html', {'loans': loans})


# this view handles the authentication process, rendering the correct view for the user.
def chose_login(request):
    logged_user = request.user
    email = logged_user.email
    try:
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
