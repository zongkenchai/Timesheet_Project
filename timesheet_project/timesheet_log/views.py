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
class TimesheetLogListView(ListView):
    template_name = 'timesheet_log_view.html'
    model = TimesheetLog
    context_object_name = 'timesheet_log'
    
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


class TimesheetLogCreateView(CreateView):
    template_name = 'timesheet_log_form.html'
    form_class = TimesheetLogForm
    model = TimesheetLog
    success_message = "Successfully Created Logs"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('timesheet_log_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class TimesheetLogUpdateView(UpdateView):
    template_name = 'timesheet_log_form.html'
    form_class = TimesheetLogForm
    model = TimesheetLog
    success_message = "Successfully Updated Logs"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('timesheet_log_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


def delete_timesheet_log(request, pk):
    if request.method=="GET":
        timesheet_log = TimesheetLog.objects.get(id=pk)
        messages.error(request, f"Successfully deleted Log - {timesheet_log.id}")
        timesheet_log.delete()
        return HttpResponseRedirect(reverse('timesheet_log_list'))