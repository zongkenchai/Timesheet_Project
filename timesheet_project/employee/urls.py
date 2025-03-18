from django.urls import path
from .views import *


urlpatterns = [
    path("", EmployeeListView.as_view(), name="employee_list"),
    path("create/", EmployeeCreateView.as_view(), name="employee_create"),
    path("edit/<slug:pk>/", EmployeeUpdateView.as_view(), name="employee_edit"),
    path("detail/<slug:pk>/", EmployeeDetailView.as_view(), name="employee_detail"),
    path("delete/<slug:pk>/", delete_employee, name="employee_delete"),
    path("salary-record/create/<int:employee_id>", SalaryRecordCreateView.as_view(), name='salary_record_create'),
    path("salary-record/edit/<slug:pk>/<int:employee_id>/", SalaryRecordUpdateView.as_view(), name='salary_record_edit'),
    path("salary-record/delete/<slug:pk>/<int:employee_id>/", delete_salary_record, name='salary_record_delete'),
]