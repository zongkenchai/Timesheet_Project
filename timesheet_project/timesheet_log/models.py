from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from employee.models import *
from project.models import *
# Create your models here.

class TimesheetLog(models.Model):
    fk_employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None)
    fk_project_id = models.ForeignKey(Project, on_delete=models.DO_NOTHING, default=None)
    date = models.DateField(default=timezone.now, null=False, blank=False)
    duration = models.DurationField(blank=False, null=False, default=datetime.timedelta)