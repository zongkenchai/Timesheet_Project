from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from project.models import *
from django.core.exceptions import ValidationError

class ProjectIncome(models.Model):
    invoice_no = models.CharField(max_length=100, blank=False, null=False)
    invoice_date = models.DateField(null=False, blank=False)
    fk_project_id = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=100, decimal_places = 2, null=False, blank=False)
    
    def __str__(self):
        return f'INV/{self.fk_project_id.project_code}/{self.invoice_no}'

    class Meta:
        unique_together = (
            (
                'fk_project_id',
                'invoice_no'
            )
        )
     
     
def validate_file_extension(value):
    valid_extensions = ['csv', 'xls', 'xlsx']  # List of valid file extensions
    file_extension = str(value).split('.')[-1].lower()
    if file_extension not in valid_extensions:
        raise ValidationError(
            ('File type not supported. Please upload a CSV, XLS, or XLSX file.')
        )
           
class ProjectIncomeUploadFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/project_income/', validators=[validate_file_extension])

    @property
    def file_extension(self):
        return str(self.file).split('.')[-1].lower()