from django.db import models
from django.utils import timezone
from company.models import Company
# Create your models here.
class Project(models.Model):
    project_code = models.CharField(max_length=20, unique=True, blank=False)
    project_name = models.CharField(max_length=50, null=False, blank=False)
    fk_company_id = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    start_date = models.DateField(default=timezone.now, blank=False)
    end_date = models.DateField(default=None, null=True, blank=True)
    original_project_fee = models.DecimalField(max_digits=100, decimal_places = 2, null=False, blank=False)

    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.project_code} - {self.project_name}'
    
    


class ProjectPhase(models.Model):
    fk_project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    phase_name = models.CharField(max_lenght=100, blank=False, null=False)
    pic_name = models.CharField(max_length=100)

    PHASE_STATUS = [
        ('pre_tender', 'Pre-Tender'),
        ('construction', 'Construction')
        ('on_hold', 'On Hold'),
        ('final_fee_to_collect', 'Final Fee to Collect')
        ('completed', 'Completed')
    ]
    phase_status = models.CharField(choices=PHASE_STATUS)
    phase_progress = models.IntegerField()
    phase_fee = models.DecimalField(max_digits=100, decimal_places = 2) 
    phase_additional_fee = models.DecimalField(max_digits=100, decimal_places=2)
    on_hold_fee = models.DecimalField(max_digits=100, decimal_places=2)
    cancellation_fee = models.DecimalField(max_digits=100, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.fk_project_id.project_code} - {self.phase_name}'
    
class ProjectPhaseForecastRevenue(models.Model):
    fk_project_id = models.ForeignKey(ProjectPhase, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=100, decimal_places = 2, null=False, blank=False)
    