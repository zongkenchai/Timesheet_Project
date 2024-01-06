from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from position.models import *
# Create your models here.
class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    fk_position_id = models.ForeignKey(Position, on_delete=models.DO_NOTHING)
    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    ]
    gender = models.CharField(max_length=10, choices=GENDER, default='Male')
    email_address = models.EmailField(unique=True, blank=True)
    start_date = models.DateField(default=timezone.now, blank=False)
    end_date = models.DateField(default=None, null=True, blank=True)
    

    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def has_resigned(self):
        if self.end_date is not None:
            return 'Resigned'
        else:
            return 'Active'
        
    def __str__(self):
        return f'{self.employee_id}-{self.first_name} {self.last_name}'
    