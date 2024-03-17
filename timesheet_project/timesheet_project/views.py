from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.views import PasswordResetView
from django.template import RequestContext
from django.contrib.admin.models import LogEntry
from django.apps import apps
from django.contrib.auth.models import User
from django.urls import reverse,reverse_lazy
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION ,DELETION
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login, logout
from customauth.forms import NewUserForm
from customauth.models import *

class LandingPageView(LoginRequiredMixin, TemplateView):
    #landing page view that features all main initial options
    #only require login + permission checks on front end to see which buttons can be accessed
    template_name = "landing.html"