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
            "start_date" : "Start Date",
            "end_date" : "End Date",
            "expected_revenue" : "Aggreement Revenue",
            }
        

class ProjectPhaseForecastRevenueForm(ModelForm):

    class Meta:
        model = ProjectPhaseForecastRevenue
        fields = '__all__'
        labels = {
            "fk_prokect_id" : "Project",
            "year" : "Year",
            "revenue_target" : 'Revenue Target',
            }