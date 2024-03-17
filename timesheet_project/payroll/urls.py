from django.urls import path
from .views import *


urlpatterns = [
    path("", PayrollListView.as_view(), name="payroll_list"),
    path("create/", PayrollCreateView.as_view(), name="payroll_create"),
    path("edit/<slug:pk>/", PayrollUpdateView.as_view(), name="payroll_edit"),
    path("delete/<slug:pk>/", delete_payroll, name="payroll_delete"),
    path("upload/", upload_file, name='payroll_upload')
]