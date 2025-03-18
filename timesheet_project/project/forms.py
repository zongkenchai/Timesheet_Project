from django import forms
from django.forms import ModelForm, TextInput
from .models import *

    
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        labels = {
            "project_code" : "Project Code",
            "project_name" : "Project Name",
            "fk_company_id" : 'Customer Name',
            "fk_project_manager_id" : 'Project Manager',
            "start_date" : "Start Date",
            "end_date" : "End Date",
            "original_project_fee" : "Project Fee",
            }
       

class ProjectPhaseForm(ModelForm):

    class Meta:
        model = ProjectPhase
        fields = '__all__'
        labels = {
            "fk_project_id" : "Project",
            "phase_name" : "Phase",
            "pic_name" : 'PIC Name',
            'phase_start_date' : 'Start Date',
            'phase_end_date' : 'End Date',
            'phase_status' : 'Status',
            'phase_progress' : 'Progress',
            'phase_fee' : 'Fee',
            'additional_fee' : 'Additional Fee',
            'on_hold_fee' : 'On Hold Fee',
            'cancellation_fee' : 'Cancellation Fee',
            'notes' : 'Internal Notes'
            } 



class ProjectPhaseForecastRevenueForm(ModelForm):

    class Meta:
        model = ProjectPhaseForecastRevenue
        fields = '__all__'
        labels = {
            "fk_project_phase_id" : "Project Phase",
            "date" : "Year Month",
            "amount" : 'Forecast Revenue',
            }