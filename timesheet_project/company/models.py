from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers
# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    # pic_name = models.CharField(max_length=50, blank=False, null=False)
    contact = PhoneNumberField(blank=True, null=True)
    pic_email_address = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.company_name

    @property
    def formatted_phone(self):
        if self.contact:
            parsed_number = phonenumbers.parse(str(self.contact), None)
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            return formatted_number
        return None