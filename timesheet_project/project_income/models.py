from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from project.models import *
from django.core.exceptions import ValidationError

class ProjectInvoice(models.Model):
    invoice_no = models.CharField(max_length=100, blank=False, null=False)
    invoice_date = models.DateField(null=False, blank=False, default=timezone.now)
    fk_project_id = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=100, decimal_places = 2, null=False, blank=False)
    
    IS_CANCELLED = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]
    
    is_cancelled = models.CharField(choices=IS_CANCELLED, default='no')
    
    def __str__(self):
        return f'{self.invoice_no}'

    @property
    def amount_paid(self):
        project_payment = ProjectPayment.objects.filter(fk_invoice_id=self.id)
        amount_paid = sum([i.amount for i in project_payment])
        return amount_paid
    
    @property
    def amount_outstanding(self):
        project_payment = ProjectPayment.objects.filter(fk_invoice_id=self.id)
        amount_outstanding = self.amount - sum([i.amount for i in project_payment])
        return amount_outstanding

    class Meta:
        unique_together = (
            (
                'fk_project_id',
                'invoice_no'
            )
        )
        
        
class ProjectPayment(models.Model):
    fk_invoice_id = models.ForeignKey(ProjectInvoice, on_delete=models.DO_NOTHING)
    payment_no = models.CharField(max_length=20, unique=True)
    payment_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=100, decimal_places = 2, null=False, blank=False)
    
    def __str__(self):
        return self.payment_no
    
     
def validate_file_extension(value):
    valid_extensions = ['csv', 'xls', 'xlsx']  # List of valid file extensions
    file_extension = str(value).split('.')[-1].lower()
    if file_extension not in valid_extensions:
        raise ValidationError(
            ('File type not supported. Please upload a CSV, XLS, or XLSX file.')
        )
           
class ProjectInvoiceUploadFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/project_invoice/', validators=[validate_file_extension])

    @property
    def file_extension(self):
        return str(self.file).split('.')[-1].lower()
class ProjectPaymentUploadFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/project_payment/', validators=[validate_file_extension])

    @property
    def file_extension(self):
        return str(self.file).split('.')[-1].lower()