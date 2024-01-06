from django import forms
from django.forms import ModelForm, TextInput
from .models import *

# class EmployeeWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "employee_id__icontains",
#         "full_name__icontains",
#     ]


class PayrollForm(ModelForm):
    class Meta:
        model = Payroll
        fields = '__all__'
        labels = {
            "fk_employee_id" : "Employee",
            "date" : "Payroll Date",
            "amount" : "Salary",
            }
        


