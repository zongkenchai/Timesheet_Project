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
from project.models import Project
#! Position Main View
#TODO : Add sorting, permissions
class ProjectInvoiceListView(PermissionRequiredMixin, ListView):
    template_name = 'project_invoice_view.html'
    model = ProjectInvoice
    permission_required = 'project_income.view_projectinvoice'
    context_object_name = 'project_invoice'
    
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


class ProjectInvoiceCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project_invoice_form.html'
    form_class = ProjectInvoiceForm
    model = ProjectInvoice
    permission_required = 'project_income.add_projectinvoice'
    success_message = "Successfully Created Invoice"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_invoice_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectInvoiceUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project_invoice_form.html'
    form_class = ProjectInvoiceForm
    model = ProjectInvoice
    permission_required = 'project_income.change_projectinvoice'
    success_message = "Successfully Updated Income"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_invoice_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

@permission_required('project_income.delete_projectinvoice', raise_exception=True)
def delete_project_invoice(request, pk):
    if request.method=="GET":
        project_invoice = ProjectInvoice.objects.get(id=pk)
        messages.error(request, f"Successfully deleted Invoice - {project_invoice.id}")
        project_invoice.delete()
        return HttpResponseRedirect(reverse('project_invoice_list'))
    
    
    

#! Handling the file upload
@permission_required('project_income_upload.add_projectinvoiceuploadfile')
def upload_file(request):
    if request.method == 'POST':
        form = ProjectInvoiceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            print(instance)
            if instance.file_extension == 'csv':
                df = pd.read_csv(instance.file.path)
            elif instance.file_extension == 'xlsx':
                df = pd.read_excel(instance.file.path)
                
            print(Project.objects.get(project_code='bsb-123'))
            list_to_create = [
                ProjectInvoice(
                    invoice_no = row['invoice_no'],
                    invoice_date = row['invoice_date'],
                    fk_project_id = Project.objects.get(project_code=row["project_code"]),
                    amount = row['amount']
                )
                for index, row in df.iterrows() if Project.objects.filter(project_code=row["project_code"]).exists()
                ]
            print(list_to_create)
            try:
                ProjectInvoice.objects.bulk_create(
                    list_to_create,
                    update_conflicts=True,
                    update_fields=['amount'],
                    unique_fields=['invoice_no', 'fk_project_id']
                )
                messages.success(request, f"Successfully uploaded file")
            except IntegrityError:
                messages.warning(request, f"File uploaded contain duplicates values. Please check the file")
            return HttpResponseRedirect(reverse('project_invoice_list'))
        
        else:
            context = {'form' : form}
            return render(request, 'project_invoice_upload.html', context)
        
    context = context = {'form' : ProjectInvoiceUploadForm()}
    return render(request, 'project_invoice_upload.html', context)
    


class ProjectPaymentListView(PermissionRequiredMixin, ListView):
    template_name = 'project_payment_view.html'
    model = ProjectPayment
    permission_required = 'project_income.view_projectpayment'
    context_object_name = 'project_payment'
    
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


class ProjectPaymentCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project_payment_form.html'
    form_class = ProjectPaymentForm
    model = ProjectPayment
    permission_required = 'project_income.add_projectpayment'
    success_message = "Successfully Created Payment"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_payment_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectPaymentUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project_payment_form.html'
    form_class = ProjectPaymentForm
    model = ProjectPayment
    permission_required = 'project_income.change_projectpayment'
    success_message = "Successfully Updated Payment"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_payment_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

@permission_required('project_income.delete_projectpayment', raise_exception=True)
def delete_project_payment(request, pk):
    if request.method=="GET":
        project_payment = ProjectPayment.objects.get(id=pk)
        messages.error(request, f"Successfully deleted Payment - {project_payment.id}")
        project_payment.delete()
        return HttpResponseRedirect(reverse('project_payment_list'))



#! Handling the file upload
@permission_required('project_income_upload.add_projectpaymentuploadfile')
def upload_file_project_payment(request):
    if request.method == 'POST':
        form = ProjectPaymentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            print(instance)
            if instance.file_extension == 'csv':
                df = pd.read_csv(instance.file.path)
            elif instance.file_extension == 'xlsx':
                df = pd.read_excel(instance.file.path)
                
            list_to_create = [
                ProjectPayment(
                    fk_invoice_id = ProjectInvoice.objects.get(invoice_no=row["invoice_no"]),
                    payment_no = row['payment_no'],
                    payment_date = row['payment_date'],
                    amount = row['amount']
                )
                for index, row in df.iterrows() if ProjectInvoice.objects.get(invoice_no=row["invoice_no"]).exists()
                ]
            print(list_to_create)
            try:
                ProjectPayment.objects.bulk_create(
                    list_to_create,
                    update_conflicts=True,
                    update_fields=['amount'],
                    unique_fields=['fk_invoice_no', 'payment_no']
                )
                messages.success(request, f"Successfully uploaded file")
            except IntegrityError:
                messages.warning(request, f"File uploaded contain duplicates values. Please check the file")
            return HttpResponseRedirect(reverse('project_payment_list'))
        
        else:
            context = {'form' : form}
            return render(request, 'project_payment_upload.html', context)
        
    context = context = {'form' : ProjectPaymentUploadForm()}
    return render(request, 'project_payment_upload.html', context)