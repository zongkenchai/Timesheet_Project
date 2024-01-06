from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from employee.models import *

class Payroll(models.Model):
    fk_employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    date = models.DateField(default=timezone.now, blank=False)
    amount = models.DecimalField(max_digits=100, decimal_places = 2, null=False, blank=False)
    
    @property
    def payroll_month(self):
        return self.date.strftime('%y-%b')