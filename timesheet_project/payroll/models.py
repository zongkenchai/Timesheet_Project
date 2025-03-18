from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from employee.models import *
from django.core.exceptions import ValidationError

class Payroll(models.Model):
    fk_employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    date = models.DateField(default=timezone.now, blank=False)
    amount = models.DecimalField(max_digits=100, decimal_places = 2, null=False, blank=False)
    
    @property
    def payroll_month(self):
        return self.date.strftime('%y-%b')
    
    class Meta:
        unique_together = (
            (
                'fk_employee_id',
                'date'
            )
        )
     
    
def validate_file_extension(value):
    valid_extensions = ['csv', 'xls', 'xlsx']  # List of valid file extensions
    file_extension = str(value).split('.')[-1].lower()
    if file_extension not in valid_extensions:
        raise ValidationError(
            ('File type not supported. Please upload a CSV, XLS, or XLSX file.')
        )
           
class PayrollUploadFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/payroll_income/', validators=[validate_file_extension])

    @property
    def file_extension(self):
        return str(self.file).split('.')[-1].lower()

