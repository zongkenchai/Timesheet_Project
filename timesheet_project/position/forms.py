from django import forms
from django.forms import ModelForm, TextInput
from .models import *

class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = '__all__'
        labels = {
            "title" : "Title",
            "department" : "Department",
            }
        

