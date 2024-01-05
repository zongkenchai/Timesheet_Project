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
            "start_date" : "Start Date",
            "end_date" : "End Date",
            "expected_revenue" : "Expected Revenue",
            }

