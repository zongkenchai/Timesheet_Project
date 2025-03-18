from django import forms
from django.forms import ModelForm, TextInput
from customauth.models import *


class UserManagementForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ["user_name", "email", "is_email_verified","is_superuser","groups"]
        labels = {
            "user_name" : "Username",
            "email" : "Email",
            "is_email_verified" : "Email Verified?",
            "is_superuser" : "Superuser?",
            "groups": "Group Permissions"
            }
        
