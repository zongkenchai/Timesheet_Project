from django import forms
from django.forms import ModelForm, TextInput
from .models import *

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        labels = {
            "name" : "Department Name",
            }
        

