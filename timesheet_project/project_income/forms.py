from django import forms
from django.forms import ModelForm, TextInput
from .models import *

# class EmployeeWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "employee_id__icontains",
#         "full_name__icontains",
#     ]


class ProjectInvoiceForm(ModelForm):
    class Meta:
        model = ProjectInvoice
        fields = '__all__'
        labels = {
            "invoice_no" : "Invoice No.",
            "invoice_date" : "Invoice Date",
            "fk_project_id" : "Project Code",
            "amount" : "Amount",
            }
        


class ProjectPaymentForm(ModelForm):
    class Meta:
        model = ProjectPayment
        fields = '__all__'
        labels = {
            "fk_invoice_id" : "Invoice No.",
            "payment_no" : "Payment No.",
            "payment_date" : "Payment Date",
            "amount" : "Amount",
            }
        
        
class ProjectInvoiceUploadForm(ModelForm):
    class Meta:
        model = ProjectInvoiceUploadFile
        fields = ['file']
        

class ProjectPaymentUploadForm(ModelForm):
    class Meta:
        model = ProjectPaymentUploadFile
        fields = ['file']