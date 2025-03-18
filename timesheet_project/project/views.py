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

from project.models import Project

from .models import *
from .forms import *
from timesheet_log.models import *
from project_income.models import *
from employee.models import *
from project.models import *

#! Position Main View
#TODO : Add sorting, permissions
class ProjectListView(PermissionRequiredMixin, ListView):
    template_name = 'project_view.html'
    model = Project
    permission_required = 'project.view_project'
    context_object_name = 'project'

class ProjectCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project_form.html'
    form_class = ProjectForm
    model = Project
    permission_required = 'project.add_project'
    success_message = "Successfully Created Project"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project_form.html'
    form_class = ProjectForm
    model = Project
    permission_required = 'project.change_project'
    success_message = "Successfully Updated Project"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

@permission_required('project.delete_project', raise_exception=True)
def delete_project(request, pk):
    if request.method=="GET":
        project = Project.objects.get(id=pk)
        messages.error(request, f"Successfully deleted {project.project_code}")
        project.delete()
        return HttpResponseRedirect(reverse('project_list'))
    
    
class ProjectDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'project_detail.html'
    model = Project
    context_object_name = 'project'
    permission_required = 'project.view_project'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        project = context["project"]
        project_phase = ProjectPhase.objects.filter(fk_project_id=project.id)
        ####################################################
        project_timesheet = TimesheetLog.objects.filter(fk_project_id=project.id)
        
        data = {}
        if project_timesheet:
            duration_by_month = project_timesheet\
                .annotate(month=TruncMonth('date'))\
                .values('month')\
                .annotate(duration = Sum('duration'), employee_count = Count('fk_employee_id'))
            
            duration_by_month_n_employee = project_timesheet\
                .annotate(month=TruncMonth('date'))\
                .values('month', 'fk_employee_id__employee_code')\
                .annotate(duration=Sum('duration'))
                
            total_duration = project_timesheet.aggregate(Sum('duration'))
            total_employee_worked_on = project_timesheet.aggregate(Count('fk_employee_id'))
            
        else:
            duration_by_month = None
            duration_by_month_n_employee = None
            total_duration = 0
            total_employee_worked_on = 0
                
                
                
                
        project_invoice_df = ProjectInvoice.objects.filter(fk_project_id=project.id)
        project_invoice_ids = [i.id for i in ProjectInvoice.objects.all().filter(fk_project_id=project.id)]
        project_payment_df = ProjectPayment.objects.filter(fk_invoice_id__in=project_invoice_ids)
        

        total_invoice_amount = sum([i.amount for i in project_invoice_df])
        total_payment_amount = sum([i.amount for i in project_payment_df])
        total_outstanding_amount = total_invoice_amount - total_payment_amount
        
        project_phase_ids = [i.id for i in  ProjectPhase.objects.all().filter(fk_project_id=project.id)]
        project_forecast_revenue = ProjectPhaseForecastRevenue.objects.filter(fk_project_phase_id__in=project_phase_ids)\
            .annotate(month=TruncMonth('date'))\
            .values('month')\
            .annotate(amount=Sum('amount'))

        print(project_forecast_revenue)

        context['project'] = project
        context['project_phase'] = project_phase
        context['project_timesheet'] = project_timesheet
        context['duration_by_month'] = duration_by_month
        context['duration_by_month_n_employee'] = duration_by_month_n_employee
        context['invoice'] = project_invoice_df
        context['payment'] = project_payment_df
        context['total_invoice_amount'] = total_invoice_amount
        context['total_payment_amount'] = total_payment_amount
        context['total_outstanding_amount'] = total_outstanding_amount
        context['total_duration'] = total_duration
        context['total_employee_worked_on'] = total_employee_worked_on
        context['project_revenue_target'] = project_forecast_revenue
            
        print(context)
        #####################################################

        return context
    


############################
class ProjectPhaseCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project_phase_form.html'
    form_class = ProjectPhaseForm
    model = ProjectPhase
    permission_required = 'project.add_projectphase'
    success_message = "Successfully Created Project Phase"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add additional variables to the context
        context['project_id'] = self.kwargs['project_id']

        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_phase_detail', kwargs = {'pk':self.object.id}) 

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_initial(self, *args, **kwargs):
        print(self)
        project = Project.objects.filter(id=self.kwargs['project_id']).first()
        return {'fk_project_id' : project.id}


class ProjectPhaseUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project_phase_form.html'
    form_class = ProjectPhaseForm
    model = ProjectPhase
    permission_required = 'project.change_projectphase'
    success_message = "Successfully Updated Project Phase"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add additional variables to the context
        context['project_id'] = self.kwargs['project_id']

        return context
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_phase_detail', kwargs = {'pk':self.object.id}) # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

@permission_required('project.delete_projectphase', raise_exception=True)
def delete_project_phase(request, pk, project_id):
    if request.method=="GET":
        project_phase = ProjectPhase.objects.get(id=pk)
        messages.error(request, f"Successfully deleted Project Phase")
        project_phase.delete()
        return HttpResponseRedirect(reverse('project_detail', kwargs = {'pk':project_id}))
    
    
class ProjectPhaseDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'project_phase_detail.html'
    model = ProjectPhase
    context_object_name = 'project_phase'
    permission_required = 'project.view_projectphase'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        project_phase = context["project_phase"]
        project_phase_forecast_revenue = ProjectPhaseForecastRevenue.objects.filter(fk_project_phase_id=project_phase.id)
        
        context['project_phase'] = project_phase
        context['project_phase_forecast_revenue'] = project_phase_forecast_revenue
        return context





class ProjectPhaseForecastRevenueCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project_phase_forecast_revenue_form.html'
    form_class = ProjectPhaseForecastRevenueForm
    model = ProjectPhaseForecastRevenue
    permission_required = 'project.add_projectphaseforecastrevenue'
    success_message = "Successfully Created Forecast Revenue"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add additional variables to the context
        context['phase_id'] = self.kwargs['phase_id']

        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_phase_detail', kwargs = {'pk':self.kwargs['phase_id']}) 

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_initial(self, *args, **kwargs):
        print(self)
        print(self.kwargs['phase_id'])
        phase = ProjectPhase.objects.filter(id=self.kwargs['phase_id']).first()
        print(phase)
        return {'fk_project_phase_id' : phase.id}
    
    
class ProjectPhaseForecastRevenueUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project_phase_forecast_revenue_form.html'
    form_class = ProjectPhaseForecastRevenueForm
    model = ProjectPhaseForecastRevenue
    permission_required = 'project.change_projectphaseforecastrevenue'
    success_message = "Successfully Updated Forecast Revenue"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add additional variables to the context
        context['phase_id'] = self.kwargs['phase_id']

        return context
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, self.success_message)
        return reverse_lazy('project_phase_detail', kwargs = {'pk':self.kwargs['phase_id']}) # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


@permission_required('project.delete_projectphaseforecastrevenue', raise_exception=True)
def delete_project_phase_forecast_revenue(request, pk, phase_id):
    if request.method=="GET":
        project_phase_forecast_revenue = ProjectPhaseForecastRevenue.objects.get(id=pk)
        messages.error(request, f"Successfully deleted Forecast Revenue")
        project_phase_forecast_revenue.delete()
        return HttpResponseRedirect(reverse('project_phase_detail', kwargs = {'pk':phase_id}))