from django import forms
from django.forms import ModelForm, TextInput
from .models import *
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# class EmployeeWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "employee_id__icontains",
#         "full_name__icontains",
#     ]


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        labels = {
            "company_name" : "Customer Name",
            "contact" : "Contact",
            "email_address" : "Email",
            }
        widgets = {
            'contact' : PhoneNumberPrefixWidget(initial="MY")
        }


