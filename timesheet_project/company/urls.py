from django.urls import path
from .views import *

urlpatterns = [
    path("", CompanyListView.as_view(), name="company_list"),
    path("create/", CompanyCreateView.as_view(), name="company_create"),
    path("edit/<slug:pk>/", CompanyUpdateView.as_view(), name="company_edit"),
    path("delete/<slug:pk>/", delete_company, name="company_delete")
]