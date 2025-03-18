# from msilib.schema import Registry
from django.contrib import admin
from django.urls import path, include
from .views import *
from django.views.generic import TemplateView

from django.contrib.auth import views

urlpatterns = [
	# path('login', login_user, name='login'),
	path("", homepage, name="homepage"),
	path("register/", register_request, name="register"),
	path("login/", login_request, name="login"),
	path("activate_user/<uidb64>/<token>", activate_user, name="activate")
]