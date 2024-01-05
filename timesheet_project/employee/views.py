from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from .models import *
from .forms import *
from .filters import * 
from timesheet_log.models import *

#! Employee Main View
#TODO : Add sorting, permissions
class EmployeeListView(ListView):
    template_name = 'employee_view.html'
    model = Employee
    context_object_name = 'employee'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filter = EmployeeFilter(self.request.GET, queryset)
        return filter.qs
    
    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = EmployeeFilter(self.request.GET, queryset)
        context["filter"] = filter
        return context


class EmployeeCreateView(CreateView):
    template_name = 'employee_form.html'
    form_class = EmployeeForm
    model = Employee
    success_message = "Successfully Created Employee"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('employee_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class EmployeeUpdateView(UpdateView):
    template_name = 'employee_form.html'
    form_class = EmployeeForm
    model = Employee
    success_message = "Successfully Updated Employee"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('employee_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class EmployeeDetailView(DetailView):
    template_name = 'employee_detail.html'
    model = Employee
    context_object_name = 'employee'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        employee = context["employee"]
        context['employee'] = employee
        ####################################################
        try:
            context['timesheet_log'] = TimesheetLog.objects.filter(fk_employee_id=employee.id)
        except TimesheetLog.DoesNotExist:
            context['timesheet_log'] = None
        #####################################################
        print(context)
        return context
    
    
    
def delete_employee(request, pk):
    if request.method=="GET":
        employee = Employee.objects.get(id=pk)
        messages.error(request, f"Successfully deleted {employee.employee_id}")
        employee.delete()
        return HttpResponseRedirect(reverse('employee_list'))