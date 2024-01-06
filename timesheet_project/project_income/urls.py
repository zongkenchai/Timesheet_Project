from django.urls import path
from .views import *


urlpatterns = [
    path("", ProjectIncomeListView.as_view(), name="project_income_list"),
    path("create/", ProjectIncomeCreateView.as_view(), name="project_income_create"),
    path("edit/<slug:pk>/", ProjectIncomeUpdateView.as_view(), name="project_income_edit"),
    path("delete/<slug:pk>/", delete_project_income, name="project_income_delete")
]