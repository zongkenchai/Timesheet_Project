from django import forms
from django.forms import ModelForm, TextInput
from .models import *

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        labels = {
            "staff_id" : "Staff ID",
            "employee_code" : 'Employee Code',
            "full_name" : "Full Name",
            "fk_position_id" : "Position",
            "fk_department_id" : "Department",
            "email_address" : "Email Address",
            "start_date" : "Date Joined",
            "end_date" : "Date Left",
            'fk_user_id' : 'Username',
            'no_of_annual_leave' : 'Annual Leave',
            'no_of_medical_leave' : 'Medical Leave',
            }
        


class SalaryRecordForm(ModelForm):
    class Meta:
        model = SalaryRecord
        fields = '__all__'
        labels = {
            "fk_employee_id" : "Staff ID",
            "salary_review_date" : 'Salary Review Date',
            "salary" : "Salary",
            "travel_allowance" : "Travel Allowance",
            "insurance" : "Insurance",
            'no_of_annual_leave' : 'Annual Leave',
            'no_of_medical_leave' : 'Medical Leave',
            }