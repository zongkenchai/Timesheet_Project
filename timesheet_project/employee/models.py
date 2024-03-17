from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from position.models import *
from customauth.models import *
# Create your models here.
class Employee(models.Model):
    staff_id = models.CharField(max_length=20, unique=True, blank=False)
    employee_code = models.CharField(max_length=20, unique=True, blank=False)
    full_name = models.CharField(max_length=50, blank=False)
    fk_position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    fk_department_id = models.ForeignKey(Department, on_delete=models.CASCADE)

    email_address = models.EmailField(unique=True, blank=True)
    start_date = models.DateField(default=timezone.now, blank=False)
    end_date = models.DateField(default=None, null=True, blank=True)
    fk_user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)


    
    @property
    def current_salary(self):
        salary_records = SalaryRecord.objects.filter(fk_staff_id=self.id).order_by('-salary_review_date')
        return salary_records.first().salary
    
    @property
    def has_resigned(self):
        if self.end_date is not None:
            return 'Resigned'
        else:
            return 'Active'
        
    def __str__(self):
        return f'{self.staff_id}-{self.employee_code}'
    
    
    
class SalaryRecord(models.Model):
    fk_employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary_review_date = models.DateField(default=timezone.now)
    salary = models.DecimalField(max_digits=100, decimal_places=2)
    travel_allowance = models.DecimalField(max_digits=100, decimal_places=2)
    insurance = models.DecimalField(max_digits=100, decimal_places=2)
    no_of_annual_leave = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    no_of_medical_leave = models.DecimalField(max_digits=100, decimal_places=2, default=0)