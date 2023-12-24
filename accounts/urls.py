"""dope URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .views import register, user_home, user_login, user_logout, edit
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', sign_up, name='front_page'),
    path('home', user_home, name='user_home'),
    path('sign-in', user_login, name='sign_in'),
    path('sign-up', register, name='sign_up'),
    path('sign-out', user_logout, name='sign_out'), 
    #path('sign-out', sign_out, name='sign_out'
    #path('social-auth/', include('social_django.urls', namespace='social')),
    path('edit/', edit, name='edit_profile')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
