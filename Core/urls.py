"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as gviews
from RegisteredUser import views as ruviews
from Admin import views as aviews
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # authentication urls
    path('admin/', admin.site.urls),
    url(r'^login/$', gviews.login, name='login'),
    url(r'^logout/$', gviews.logout, {'next_page': 'home'}),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^$', ruviews.home, name='home'),
    url(r'^register', ruviews.register, name='register'),
    url(r'^chose_login', ruviews.chose_login, name='chose_login'),
    url(r'^finish_register', ruviews.finish_register, name='finish_register'),
    url(r'^permission_denied', ruviews.permission_denied, name='permission_denied'),

    # admin urls
    url(r'^admin_dashboard', aviews.admin_dashboard, name='admin_dashboard'),
    url(r'^admin_user_search', aviews.admin_user_search, name='admin_user_search'),
    url(r'^book_management', aviews.book_management, name='book_management'),
    url(r'^smart_add', aviews.smart_add, name='smart_add'),
    url(r'^admin_profile', aviews.admin_profile, name='admin_profile'),
    url(r'^admin_about', aviews.admin_about, name='admin_about'),
    url(r'^admin_add_device', aviews.admin_add_device, name='admin_add_device'),
    url(r'^admin_admin_search', aviews.admin_admin_search, name='admin_admin_search'),
    url(r'^admin_book', aviews.admin_book, name='admin_book'),
    url(r'^admin_contact_admins', aviews.admin_contact_admins, name='admin_contact_admins'),
    url(r'^admin_contact_developers', aviews.admin_contact_developers, name='admin_contact_developers'),
    url(r'^admin_devices', aviews.admin_devices, name='admin_devices'),
    url(r'^admin_edit_admin_profile', aviews.admin_edit_admin_profile, name='admin_edit_admin_profile'),
    url(r'^admin_edit_book', aviews.admin_edit_book, name='admin_edit_book'),
    url(r'^admin_edit_my_profile', aviews.admin_edit_my_profile, name='admin_edit_my_profile'),
    url(r'^admin_edit_reader_profile', aviews.admin_edit_reader_profile, name='admin_edit_reader_profile'),
    url(r'^admin_genre', aviews.admin_genre, name='admin_genre'),
    url(r'^admin_invite_admin', aviews.admin_invite_admin, name='admin_invite_admin'),
    url(r'^admin_send_invite', aviews.admin_send_invite, name='admin_send_invite'),
    url(r'^admin_loan_page', aviews.admin_loan_page, name='admin_loan_page'),
    url(r'^admin_g_management', aviews.admin_g_management, name='admin_g_management'),
    url(r'^admin_make_loan', aviews.admin_make_loan, name='admin_make_loan'),
    url(r'^admin_manual_add', aviews.admin_manual_add, name='admin_manual_add'),
    url(r'^admin_my_profile', aviews.admin_my_profile, name='admin_my_profile'),
    url(r'^admin_reader_profile', aviews.admin_reader_profile, name='admin_reader_profile'),
    url(r'^admin_reader_search', aviews.admin_reader_search, name='admin_reader_search'),
    url(r'^admin_book', aviews.admin_search_results, name='admin_search_results'),
    url(r'^admin_terms_of_use', aviews.admin_terms_of_use, name='admin_terms_of_use'),
    url(r'^admin_view_loans', aviews.admin_view_loans, name='admin_view_loans'),
    url(r'^admin_save_book_cover/', aviews.admin_save_book_cover, name='admin_save_book_cover'),

    # reader urls

    url(r'^reader_dashboard', ruviews.reader_dashboard, name='reader_dashboard'),
    url(r'^reader_about', ruviews.reader_about, name='reader_about'),
    url(r'^reader_book', ruviews.reader_book, name='reader_book'),
    url(r'^reader_contact_admins', ruviews.reader_contact_admins, name='reader_contact_admins'),
    url(r'^reader_contact_developers', ruviews.reader_contact_developers, name='reader_contact_developers'),
    url(r'^reader_edit_my_profile', ruviews.reader_edit_my_profile, name='reader_edit_my_profile'),
    url(r'^reader_genre', ruviews.reader_genre, name='reader_genre'),
    url(r'^reader_loan_page', ruviews.reader_loan_page, name='reader_loan_page'),
    url(r'^reader_my_profile', ruviews.reader_my_profile, name='reader_my_profile'),
    url(r'^reader_search_results', ruviews.reader_search_results, name='reader_search_results'),
    url(r'^reader_terms_of_use', ruviews.reader_terms_of_use, name='reader_terms_of_use'),
    url(r'^reader_view_loans', ruviews.reader_view_loans, name='reader_view_loans'),
    url(r'^reader_books', ruviews.reader_books, name='reader_books'),
    url(r'^reader_genres', ruviews.reader_genres, name='reader_genres'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
