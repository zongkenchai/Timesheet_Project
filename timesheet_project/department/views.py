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

#! Department Main View
#TODO : Add sorting, permissions
class DepartmentListView(PermissionRequiredMixin, ListView):
    template_name = 'department_view.html'
    model = Department
    permission_required = 'department.view_department'
    context_object_name = 'department'
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     filter = EmployeeFilter(self.request.GET, queryset)
    #     return filter.qs
    
    # def get_context_data(self, **kwargs):
    #     context = super(EmployeeListView, self).get_context_data(**kwargs)
    #     queryset = self.get_queryset()
    #     filter = EmployeeFilter(self.request.GET, queryset)
    #     context["department_filter"] = filter
    #     return context


class DepartmentCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'department_form.html'
    form_class = DepartmentForm
    model = Department
    permission_required = 'department.add_department'
    success_message = "Successfully Created Department"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('department_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class DepartmentUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'department_form.html'
    form_class = DepartmentForm
    model = Department
    permission_required = 'department.chnage_department'
    success_message = "Successfully Updated Department"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('department_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

@permission_required('department.delete_department', raise_exception=True)
def delete_department(request, pk):
    if request.method=="GET":
        department = Department.objects.get(id=pk)
        messages.error(request, f"Successfully deleted {department.name}")
        department.delete()
        return HttpResponseRedirect(reverse('department_list'))