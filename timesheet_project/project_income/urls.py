from django.urls import path
from .views import *


urlpatterns = [
    path("invoice/", ProjectInvoiceListView.as_view(), name="project_invoice_list"),
    path("invoice/create/", ProjectInvoiceCreateView.as_view(), name="project_invoice_create"),
    path("invoice/edit/<slug:pk>/", ProjectInvoiceUpdateView.as_view(), name="project_invoice_edit"),
    path("invoice/delete/<slug:pk>/", delete_project_invoice, name="project_invoice_delete"),
    path("invoice/upload/", upload_file, name='project_invoice_upload'),
    path("payment/", ProjectPaymentListView.as_view(), name="project_payment_list"),
    path("payment/create/", ProjectPaymentCreateView.as_view(), name="project_payment_create"),
    path("payment/edit/<slug:pk>/", ProjectPaymentUpdateView.as_view(), name="project_payment_edit"),
    path("payment/delete/<slug:pk>/", delete_project_payment, name="project_payment_delete"),
    path("payment/upload/", upload_file_project_payment, name='project_payment_upload')
]