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
            "company_name" : "Company Name",
            "pic_name" : "PIC Name",
            "pic_contact" : "PIC Contact",
            "pic_email_address" : "PIC Email",
            }
        widgets = {
            'pic_contact' : PhoneNumberPrefixWidget(initial="MY")
        }


