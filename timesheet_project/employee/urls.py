from django.urls import path
from .views import *


urlpatterns = [
    path("", EmployeeListView.as_view(), name="employee_list"),
    path("create/", EmployeeCreateView.as_view(), name="employee_create"),
    path("edit/<slug:pk>/", EmployeeUpdateView.as_view(), name="employee_edit"),
    path("detail/<slug:pk>/", EmployeeDetailView.as_view(), name="employee_detail"),
    
]