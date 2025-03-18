from django.db import models
from django.utils import timezone
from company.models import Company
from employee.models import Employee
# Create your models here.
class Project(models.Model):
    project_code = models.CharField(max_length=20, unique=True, blank=False)
    project_name = models.CharField(max_length=50, null=False, blank=False)
    fk_project_manager_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    fk_company_id = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    start_date = models.DateField(default=timezone.now, blank=False)
    end_date = models.DateField(default=None, null=True, blank=True)
    original_project_fee = models.DecimalField(max_digits=100, decimal_places = 2, null=False, blank=False)

    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.project_code} - {self.project_name}'
    
    
    @property
    def total_phase_fee(self):
        project_phase = ProjectPhase.objects.filter(fk_project_id=self.id)
        total_phase_fee = sum([i.phase_fee for i in project_phase])
        return total_phase_fee
    
    
    @property
    def total_phase_additional_fee(self):
        project_phase = ProjectPhase.objects.filter(fk_project_id=self.id)
        total = sum([i.phase_additional_fee for i in project_phase])
        return total
    
    @property
    def total_phase_on_hold_fee(self):
        project_phase = ProjectPhase.objects.filter(fk_project_id=self.id)
        total = sum([i.on_hold_fee for i in project_phase])
        return total
    
    @property
    def total_phase_cancellation_fee(self):
        project_phase = ProjectPhase.objects.filter(fk_project_id=self.id)
        total = sum([i.cancellation_fee for i in project_phase])
        return total

class ProjectPhase(models.Model):
    fk_project_id = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    phase_name = models.CharField(max_length=100, blank=False, null=False)
    pic_name = models.CharField(max_length=100)
    phase_start_date = models.DateField(null=False, blank=False)
    phase_end_date = models.DateField(null=True, blank=True)
    PHASE_STATUS = [
        ('pre_tender', 'Pre-Tender'),
        ('construction', 'Construction'),
        ('on_hold', 'On Hold'),
        ('adhoc', 'Ad-hoc'),
        ('final_fee_to_collect', 'Final Fee to Collect'),
        ('completed', 'Completed')
    ]
    phase_status = models.CharField(choices=PHASE_STATUS)
    phase_progress = models.IntegerField(null=True, blank=True)
    phase_fee = models.DecimalField(max_digits=100, decimal_places = 2) 
    phase_additional_fee = models.DecimalField(max_digits=100, decimal_places=2)
    on_hold_fee = models.DecimalField(max_digits=100, decimal_places=2)
    cancellation_fee = models.DecimalField(max_digits=100, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.fk_project_id.project_code} - {self.phase_name}'
    
class ProjectPhaseForecastRevenue(models.Model):
    fk_project_phase_id = models.ForeignKey(ProjectPhase, on_delete=models.DO_NOTHING)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=100, decimal_places = 2, null=False, blank=False)
