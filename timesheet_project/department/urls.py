from django.urls import path
from .views import *


urlpatterns = [
    path("", DepartmentListView.as_view(), name="department_list"),
    path("create/", DepartmentCreateView.as_view(), name="department_create"),
    path("edit/<slug:pk>/", DepartmentUpdateView.as_view(), name="department_edit"),
    path("delete/<slug:pk>/", delete_department, name="department_delete")
]