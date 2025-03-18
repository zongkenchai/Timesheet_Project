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
class TimesheetLogListView(PermissionRequiredMixin, ListView):
    template_name = 'timesheet_log_view.html'
    model = TimesheetLog
    permission_required = 'timesheet_log.view_timesheetlog'
    context_object_name = 'timesheet_log'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Check if the user is an admin
        if self.request.user.is_staff or self.request.user.groups.filter(name='Manager').exists():
            # Admin can see all records
            return queryset
        else:
            try:
                request_user = self.request.user
                correspondence_employee = Employee.objects.filter(fk_user_id=request_user.id).first()
                return queryset.filter(fk_employee_id=correspondence_employee.id)
            except AttributeError:
                return queryset
    
    def get_context_data(self, **kwargs):
        context = super(TimesheetLogListView, self).get_context_data(**kwargs)
        # request_user = self.request.user
        # correspondence_employee = Employee.objects.filter(fk_user_id=request_user.id).first()
        # context["timesheet_log"] = TimesheetLog.objects.filter(fk_employee_id=)
        context['is_admin'] = self.request.user.is_staff

        return context


class TimesheetLogCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'timesheet_log_form.html'
    form_class = TimesheetLogForm
    model = TimesheetLog
    permission_required = 'timesheet_log.add_timesheetlog'
    success_message = "Successfully Created Logs"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('timesheet_log_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        print(self.request.user.id)
        
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self) -> dict[str, Any]:
        try:
            request_user = self.request.user
            correspondence_employee = Employee.objects.filter(fk_user_id=request_user.id).first()
            return {'fk_employee_id' : correspondence_employee.id}
        except AttributeError:
            return {}


class TimesheetLogUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'timesheet_log_form.html'
    form_class = TimesheetLogForm
    model = TimesheetLog
    permission_required = 'timesheet_log.change_timesheetlog'
    success_message = "Successfully Updated Logs"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('timesheet_log_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

@permission_required('timesheet_log.delete_timesheetlog', raise_exception=True)
def delete_timesheet_log(request, pk):
    if request.method=="GET":
        timesheet_log = TimesheetLog.objects.get(id=pk)
        messages.error(request, f"Successfully deleted Log - {timesheet_log.id}")
        timesheet_log.delete()
        return HttpResponseRedirect(reverse('timesheet_log_list'))