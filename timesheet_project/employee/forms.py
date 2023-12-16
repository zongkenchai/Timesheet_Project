from django import forms
from django.forms import ModelForm, TextInput
from .models import *

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        labels = {
            "employee_id" : "Employee ID",
            "first_name" : "First Name",
            "last_name" : "Last Name",
            "fk_position_id" : "Title",
            "gender" : "Gender",
            "email_address" : "Email Address",
            "start_date" : "Date Joined",
            "end_date" : "Date Left",
            }
        

