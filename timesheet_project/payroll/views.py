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
from django.db import IntegrityError
from .models import *
from .forms import *
import pandas as pd
from employee.models import *
#! Position Main View
#TODO : Add sorting, permissions
class PayrollListView(PermissionRequiredMixin, ListView):
    template_name = 'payroll_view.html'
    model = Payroll
    permission_required = 'payroll.view_payroll'
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


class PayrollCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'payroll_form.html'
    form_class = PayrollForm
    model = Payroll
    permission_required = 'payroll.add_payroll'
    success_message = "Successfully Created Payroll"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('payroll_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class PayrollUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'payroll_form.html'
    form_class = PayrollForm
    model = Payroll
    permission_required = 'payroll.change_payroll'
    success_message = "Successfully Updated Payroll"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('payroll_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

@permission_required('payroll.delete_payroll', raise_exception=True)
def delete_payroll(request, pk):
    if request.method=="GET":
        payroll = Payroll.objects.get(id=pk)
        messages.error(request, f"Successfully deleted Income - {payroll.id}")
        payroll.delete()
        return HttpResponseRedirect(reverse('payroll_list'))
    
    
#! Handling the file upload
@permission_required('payroll_upload.add_payroll_upload', raise_exception=True)
def upload_file(request):
    if request.method == 'POST':
        form = PayrollUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            print(instance)
            if instance.file_extension == 'csv':
                df = pd.read_csv(instance.file.path)
            elif instance.file_extension == 'xlsx':
                df = pd.read_excel(instance.file.path)
                
            # print(Employee.objects.get(empl='bsb-123'))
            list_to_create = [
                Payroll(
                    fk_employee_id = Employee.objects.get(employee_id=row["employee_code"]),
                    date = row['date'],
                    amount = row['amount']
                )
                for index, row in df.iterrows() if Employee.objects.filter(employee_id=row["employee_code"]).exists()
                ]
            print(list_to_create)
            try:
                Payroll.objects.bulk_create(
                    list_to_create,
                    update_conflicts=True,
                    update_fields=['amount'],
                    unique_fields=['fk_employee_id', 'date']
                )
                messages.success(request, f"Successfully uploaded file")
            except IntegrityError:
                messages.warning(request, f"File uploaded contain duplicates values. Please check the file")
            return HttpResponseRedirect(reverse('payroll_list'))
        
        else:
            context = {'form' : form}
            return render(request, 'payroll_upload.html', context)
        
    context = context = {'form' : PayrollUploadForm()}
    return render(request, 'payroll_upload.html', context)
    