from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from .models import *
from .forms import *

#! Position Main View
#TODO : Add sorting, permissions
class CompanyListView(PermissionRequiredMixin, ListView):
    template_name = 'company_view.html'
    model = Company
    permission_required  = "company.view_company"
    context_object_name = 'company'
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     filter = EmployeeFilter(self.request.GET, queryset)
    #     return filter.qs
    
    # def get_context_data(self, **kwargs):
    #     context = super(EmployeeListView, self).get_context_data(**kwargs)
    #     queryset = self.get_queryset()
    #     filter = EmployeeFilter(self.request.GET, queryset)
    #     context["employee_filter"] = filter
    #     return context


class CompanyCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'company_form.html'
    form_class = CompanyForm
    model = Company
    permission_required = 'company.add_company'
    success_message = "Successfully Created Company"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('company_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class CompanyUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'company_form.html'
    form_class = CompanyForm
    model = Company
    permission_required = 'company.change_company'
    success_message = "Successfully Updated Company"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('company_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


@permission_required('company.delete_company',raise_exception=True)
def delete_company(request, pk):
    if request.method=="GET":
        company = Company.objects.get(id=pk)
        messages.error(request, f"Successfully deleted Company - {company.id}")
        company.delete()
        return HttpResponseRedirect(reverse('company_list'))