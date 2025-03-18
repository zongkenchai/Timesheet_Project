from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from department.models import Department


class Position(models.Model):
    position = models.CharField(max_length=50, blank=False, null=False, unique=True)
    
    def __str__(self):
        return f'{self.position}'


