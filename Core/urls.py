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
    # authentication process urls
    path('admin/', admin.site.urls),
    url(r'^login/$', gviews.login, name='login'),
    url(r'^logout/$', gviews.logout, {'next_page': 'home'}),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^$', ruviews.home, name='home'),
    url(r'^register', ruviews.register, name='register'),
    url(r'^chose_login', ruviews.chose_login, name='chose_login'),
    url(r'^finish_register', ruviews.finish_register, name='finish_register'),
    url(r'^permission_denied', ruviews.permission_denied, name='permission_denied'),
    url(r'^redirect_to_app', ruviews.redirect_to_app, name='redirect_to_app'),

    # web services
    url(r'^is_logged_in', ruviews.is_logged_in, name='is_logged_in'),
    url(r'^is_administrator', ruviews.is_administrator, name='is_administrator'),
    url(r'^get_user_info', ruviews.get_user_info, name='get_user_info'),
    url(r'^get_categories', ruviews.get_categories, name='get_categories'),

    # admin web services
    url(r'^invite_administrator', ruviews.invite_administrator, name='invite_administrator'),
    url(r'^create_category', aviews.create_category, name='create_category'),
    url(r'^delete_category', aviews.delete_category, name='delete_category'),
    url(r'^edit_category', aviews.edit_category, name='edit_category'),
    url(r'^add_book', aviews.add_book, name='add_book'),
]

#if settings.DEBUG: # settings to make static and media files work
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
