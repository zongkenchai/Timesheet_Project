from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from project.models import *
from company.models import *
# Create your models here.
# class ProjectIncome(models.Model):
#     fk_project_id = models.ForeignKey(Project, on_delete=models.DO_NOTHING, default=None)
#     fk_company_id = models.ForeignKey(Project,on_delete=models.DO_NOTHING, default=None)
#     invoice_no = models.CharField(max_length=100, blank=False, null=False)
#     invoice_date = models.DateField(null=False, blank=False)
#     amount = models.FloatField(default=0, null=False, blank=False)
    
#     def __str__(self):
#         return f'INV/{self.fk_project_id.project_code}/{self.invoice_no}'

#     class Meta:
#         unique_together = (
#             (
#                 'fk_project_id',
#                 'fk_company_id',
#                 'invoice_no'
#             )
#         )
