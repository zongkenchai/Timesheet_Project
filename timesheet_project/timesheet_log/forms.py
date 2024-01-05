from django import forms
from django.forms import ModelForm, TextInput
from .models import *

# class EmployeeWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "employee_id__icontains",
#         "full_name__icontains",
#     ]
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


