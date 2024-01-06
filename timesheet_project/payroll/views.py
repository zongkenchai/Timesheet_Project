# Create your views here.
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
class PayrollListView(ListView):
    template_name = 'payroll_view.html'
    model = Payroll
    context_object_name = 'payroll'
    
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


class PayrollCreateView(CreateView):
    template_name = 'payroll_form.html'
    form_class = PayrollForm
    model = Payroll
    success_message = "Successfully Created Logs"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('payroll_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class PayrollUpdateView(UpdateView):
    template_name = 'payroll_form.html'
    form_class = PayrollForm
    model = Payroll
    success_message = "Successfully Updated Logs"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('payroll_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


def delete_payroll(request, pk):
    if request.method=="GET":
        payroll = Payroll.objects.get(id=pk)
        messages.error(request, f"Successfully deleted Income - {payroll.id}")
        payroll.delete()
        return HttpResponseRedirect(reverse('payroll_list'))