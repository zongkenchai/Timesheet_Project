from django import forms
from django.forms import ModelForm, TextInput
from .models import *

class TimesheetLogForm(ModelForm):
    class Meta:
        model = TimesheetLog
        fields = '__all__'
        labels = {
            "fk_employee_id" : "Employee ID",
            "fk_project_id" : "Project ID",
            "date" : "Date",
            "duration" : "Duration (h:m:s)",
            }
        

