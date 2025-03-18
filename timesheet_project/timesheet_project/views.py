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
from django.contrib.auth.models import Group, Permission
from .forms import *

class LandingPageView(LoginRequiredMixin, TemplateView):
    #landing page view that features all main initial options
    #only require login + permission checks on front end to see which buttons can be accessed
    template_name = "landing.html"
    
    
class AdminManageRolesAccessView(PermissionRequiredMixin, TemplateView):
    template_name = 'admin_manageaccess.html'
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super(AdminManageRolesAccessView, self).get_context_data(**kwargs)
        context['users'] = MyUser.objects.all()
        return context

class AdminManageRolesAccessUpdateView(UpdateView,PermissionRequiredMixin):
    template_name = 'admin_manageaccess_edit.html'
    model = MyUser
    permission_required = "is_staff"
    form_class = UserManagementForm

    def get_success_url(self):
        messages.success(self.request, f"Successfully Updated User")
        return reverse_lazy('admin_manage')
    
    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    
def handler403(request, *args, **argv):
    response = render(request, '403.html', {})
    response.status_code = 403
    return response
