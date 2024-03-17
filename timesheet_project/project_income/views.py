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
class ProjectIncomeListView(PermissionRequiredMixin, ListView):
    template_name = 'project_income_view.html'
    model = ProjectIncome
    permission_required = 'project_income.view_project_income'
    context_object_name = 'project_income'
    
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


class ProjectIncomeCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project_income_form.html'
    form_class = ProjectIncomeForm
    model = ProjectIncome
    permission_required = 'project_income.add_project_income'
    success_message = "Successfully Created Income"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_income_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectIncomeUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project_income_form.html'
    form_class = ProjectIncomeForm
    model = ProjectIncome
    permission_required = 'project_income.change_project_income'
    success_message = "Successfully Updated Income"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_income_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

@permission_required('project_income.delete_project_income', raise_exception=True)
def delete_project_income(request, pk):
    if request.method=="GET":
        project_income = ProjectIncome.objects.get(id=pk)
        messages.error(request, f"Successfully deleted Income - {project_income.id}")
        project_income.delete()
        return HttpResponseRedirect(reverse('project_income_list'))
    
    
    

#! Handling the file upload
@permission_required('project_income_upload.add_project_income_upload')
def upload_file(request):
    if request.method == 'POST':
        form = ProjectIncomeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            print(instance)
            if instance.file_extension == 'csv':
                df = pd.read_csv(instance.file.path)
            elif instance.file_extension == 'xlsx':
                df = pd.read_excel(instance.file.path)
                
            print(Project.objects.get(project_code='bsb-123'))
            list_to_create = [
                ProjectIncome(
                    invoice_no = row['invoice_no'],
                    invoice_date = row['invoice_date'],
                    fk_project_id = Project.objects.get(project_code=row["project_code"]),
                    amount = row['amount']
                )
                for index, row in df.iterrows() if Project.objects.filter(project_code=row["project_code"]).exists()
                ]
            print(list_to_create)
            try:
                ProjectIncome.objects.bulk_create(
                    list_to_create,
                    update_conflicts=True,
                    update_fields=['amount'],
                    unique_fields=['invoice_no', 'fk_project_id']
                )
                messages.success(request, f"Successfully uploaded file")
            except IntegrityError:
                messages.warning(request, f"File uploaded contain duplicates values. Please check the file")
            return HttpResponseRedirect(reverse('project_income_list'))
        
        else:
            context = {'form' : form}
            return render(request, 'project_income_upload.html', context)
        
    context = context = {'form' : ProjectIncomeUploadForm()}
    return render(request, 'project_income_upload.html', context)
    
