from django.db import models
from django.utils import timezone
from company.models import Company
# Create your models here.
class Project(models.Model):
    project_code = models.CharField(max_length=20, unique=True, blank=False)
    project_name = models.CharField(max_length=50, null=False, blank=False)
    fk_company_name = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    start_date = models.DateField(default=timezone.now, blank=False)
    end_date = models.DateField(default=None, null=True, blank=True)
    expected_revenue = models.DecimalField(max_digits=100, decimal_places = 2, null=False, blank=False)
    # description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.project_code} - {self.project_name}'