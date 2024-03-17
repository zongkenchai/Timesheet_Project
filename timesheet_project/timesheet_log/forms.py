from django import forms
from django.forms import ModelForm, TextInput
from .models import *
from employee.models import *
# class EmployeeWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "employee_id__icontains",
#         "full_name__icontains",
#     ]
class TimesheetLogForm(ModelForm):
    fk_employee_id = forms.ModelChoiceField(queryset=Employee.objects.filter(end_date=None), label='Employee ID')

    def __init(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
    class Meta:
        model = TimesheetLog
        fields = '__all__'
        labels = {
            "fk_employee_id" : "Employee ID",
            "fk_project_id" : "Project ID",
            "date" : "Date",
            "duration" : "Duration (h:m:s)",
            }


