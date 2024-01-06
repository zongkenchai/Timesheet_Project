from django import forms
from django.forms import ModelForm, TextInput
from .models import *

# class EmployeeWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "employee_id__icontains",
#         "full_name__icontains",
#     ]


class ProjectIncomeForm(ModelForm):
    class Meta:
        model = ProjectIncome
        fields = '__all__'
        labels = {
            "invoice_no" : "Invoice No",
            "invoice_date" : "Invoice Date",
            "fk_project_id" : "Project Code",
            "amount" : "Amount",
            }
        


