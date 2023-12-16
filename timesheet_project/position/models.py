from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime

class Position(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    
    DEPARTMENT = [
        ('Technical', 'Technical'),
        ('Finance', 'Finance'),
        ('HR', 'HR'),
        
    ]
    
    department = models.CharField(max_length=10, choices=DEPARTMENT, default='Technical')
    
    def __str__(self):
        return f'{self.title} ({self.department})'
    
    