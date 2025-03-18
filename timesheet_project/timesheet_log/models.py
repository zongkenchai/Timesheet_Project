from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from employee.models import *
from project.models import *
# Create your models here.

class TimesheetLog(models.Model):
    fk_employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    fk_project_id = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    date = models.DateField(default=timezone.now, null=False, blank=False)
    duration = models.DecimalField(max_digits=100, decimal_places=2)