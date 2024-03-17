from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import *
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required

# Create your views here.

# class Registration_View(ListView):
# 	template_name: "register_new_email.html"
# 	model: Registered_Email
# 	context_object_name: 'register_email'
# 	paginate_by: 10

# 	def get_queryset(self, **kwargs):
# 		qs = super().get_queryset(**kwargs)
# 		return qs.filter(is_active = 1).order_by("name")


# class Register_Email_Update_View(PermissionRequiredMixin, UpdateView):

# 	#This needs to edited
#     # permission_required  = 

#     template_name = 'register_email_edit.html'
#     model = Registered_Email
#     fields = ["email_address", "name"]

#     def get_success_url(self):
#         messages.success(self.request, f"Successfully Updated Approved Email Addresses")
#         return reverse_lazy('register_email') # kwargs = {'pk':self.object.id}



# def delete_row(request,id):
#     if request.method=="GET":
#         register_email = Registered_Email.objects.get(name=id)
#         # isolation.is_active = 0
#         register_email.save()
#         messages.error(request, f"You had deleted {register_email.email_address}")
#         return HttpResponseRedirect(reverse('register_email'))


# class RegisterEmailCreateView(PermissionRequiredMixin, CreateView):

# 	#To be edited
#     # permission_required  = 

#     template_name = 'register_email_form.html'
#     model = Registered_Email
#     fields = ["name", "email_address"]

#     def get_success_url(self):
#         messages.success(self.request, f"Successfully Approved Email Address")
#         return reverse_lazy('register_email')


# class HostInfoListView(PermissionRequiredMixin, ListView):
#     template_name = "host_info_view.html"
#     model = Host_Info
#     permission_required  = "sequencing.view_host_info"
#     context_object_name = 'host_info'
#     def get_queryset(self, **kwargs):
#         qs = super().get_queryset(**kwargs)
#         return qs.filter(is_active = 1).order_by("host_id")


class RegistrationView(ListView):
    template_name = "register_new_email.html"
    model =  RegisteredEmail
    context_object_name = 'register_email'
    # permission_required  = 'is_staff'
    
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_active = True).order_by("id")

    
class RegisterEmailUpdateView(UpdateView):

	#This needs to edited
    # permission_required  = 'is_staff'
    template_name = 'register_email_edit.html'
    model = RegisteredEmail
    fields = ["email_address", "name"]

    def get_success_url(self):
        messages.success(self.request, f"Successfully Updated Approved Email Addresses")
        return reverse_lazy('register_email') # kwargs = {'pk':self.object.id}


@permission_required('is_staff',raise_exception=True)
def delete_row(request,id):
    if request.method=="GET":
        register_email = RegisteredEmail.objects.get(id=id)
        register_email.is_active = 0
        register_email.save()
        messages.error(request, f"You had deleted {register_email.email_address}")
        return HttpResponseRedirect(reverse('register_email'))


class RegisterEmailCreateView(PermissionRequiredMixin, CreateView):

	#To be edited
    permission_required  = 'is_staff'

    template_name = 'register_email_form.html'
    model = RegisteredEmail
    fields = ["name", "email_address"]

    def get_success_url(self):
        messages.success(self.request, f"Successfully Approved Email Address")
        return reverse_lazy('register_email')