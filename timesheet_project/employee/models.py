from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
# Create your models here.
class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    email_address = models.EmailField()