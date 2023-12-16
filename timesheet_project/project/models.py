from django.db import models
from django.utils import timezone

# Create your models here.
class Project(models.Model):
    project_code = models.CharField(max_length=20, unique=True, blank=False)
    project_name = models.CharField(max_length=50, null=False, blank=False)
    start_date = models.DateField(default=timezone.now, blank=False)
    end_date = models.DateField(default=None, null=True, blank=True)
    expected_revenue = models.FloatField(null=False, blank=False)
    
    def __str__(self):
        return f'{self.project_code} - {self.project_name}'