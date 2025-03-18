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
from django.db.models import *
from django.db.models.functions import *
from django.utils.translation import gettext_lazy as _

from slick_reporting.views import *
from slick_reporting.fields import *


from .models import *
from .forms import *
from .filters import * 
from timesheet_log.models import *
from payroll.models import *
#! Employee Main View
#TODO : Add sorting, permissions
class EmployeeListView(PermissionRequiredMixin, ListView):
    template_name = 'employee_view.html'
    model = Employee
    permission_required = 'employee.view_employee'
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


class EmployeeCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'employee_form.html'
    form_class = EmployeeForm
    model = Employee
    permission_required = 'employee.add_employee'
    success_message = "Successfully Created Employee"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('employee_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class EmployeeUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'employee_form.html'
    form_class = EmployeeForm
    model = Employee
    permission_required = 'employee.change_employee'
    success_message = "Successfully Updated Employee"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('employee_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class EmployeeDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'employee_detail.html'
    model = Employee
    context_object_name = 'employee'
    permission_required = 'employee.view_employee'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        employee = context["employee"]
        context['employee'] = employee
        ####################################################
        employee_timesheet = TimesheetLog.objects.filter(fk_employee_id=employee.id)
        data = {}
        if employee_timesheet:
            duration_by_month = employee_timesheet\
                .annotate(month=TruncMonth('date'))\
                .values('fk_employee_id', 'month')\
                .annotate(duration = Sum('duration'))
            
            duration_by_month_n_project = employee_timesheet\
                .annotate(month=TruncMonth('date'))\
                .values('month', 'fk_project_id')\
                .annotate(duration=Sum('duration'))
                
        else:
            duration_by_month = None
            duration_by_month_n_project = None
                
        payroll_history = Payroll.objects.filter(fk_employee_id=employee.id)

        context['employee_timesheet'] = employee_timesheet
        context['duration_by_month'] = duration_by_month
        context['duration_by_month_n_project'] =duration_by_month_n_project
        context['payroll_history'] = payroll_history
        
        salary_record = SalaryRecord.objects.filter(fk_employee_id=employee.id)
        context['salary_record'] = salary_record
        # print(context)
        #####################################################

        return context
    
    
@permission_required('employee.delete_employee', raise_exception=True)
def delete_employee(request, pk):
    if request.method=="GET":
        employee = Employee.objects.get(id=pk)
        messages.error(request, f"Successfully deleted {employee.employee_id}")
        employee.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    




# class SalaryRecordListView(PermissionRequiredMixin, ListView):
#     template_name = 'salary_record_view.html'
#     model = SalaryRecord
#     permission_required = 'employee.view_salary_record'
#     context_object_name = 'salary_record'
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     filter = EmployeeFilter(self.request.GET, queryset)
    #     return filter.qs
    
    # def get_context_data(self, **kwargs):
    #     context = super(EmployeeListView, self).get_context_data(**kwargs)
    #     queryset = self.get_queryset()
    #     filter = EmployeeFilter(self.request.GET, queryset)
    #     context["filter"] = filter
    #     return context


class SalaryRecordCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'salary_record_form.html'
    form_class = SalaryRecordForm
    model = SalaryRecord
    permission_required = 'employee.add_salaryrecord'
    success_message = "Successfully Created Salary Record"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add additional variables to the context
        context['employee_id'] = self.kwargs['employee_id']

        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, self.success_message)
        return reverse_lazy('employee_detail', kwargs = {'pk':self.kwargs['employee_id']}) 

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_initial(self, *args, **kwargs):
        employee = Employee.objects.filter(id=self.kwargs['employee_id']).first()
        return {'fk_employee_id' : employee.id}


class SalaryRecordUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'salary_record_form.html'
    form_class = SalaryRecordForm
    model = SalaryRecord
    permission_required = 'employee.change_salaryrecord'
    success_message = "Successfully Updated Salary Record"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add additional variables to the context
        context['employee_id'] = self.kwargs['employee_id']

        return context
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, self.success_message)
        return reverse_lazy('employee_detail', kwargs = {'pk':self.kwargs['employee_id']}) # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


@permission_required('project.delete_salaryrecord', raise_exception=True)
def delete_salary_record(request, pk, employee_id):
    if request.method=="GET":
        salary_record = SalaryRecord.objects.get(id=pk)
        messages.error(request, f"Successfully deleted Revenue Target")
        salary_record.delete()
        return HttpResponseRedirect(reverse('employee_detail', kwargs = {'pk':employee_id}))