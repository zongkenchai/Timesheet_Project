from django.urls import path
from .views import *


urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("create/", ProjectCreateView.as_view(), name="project_create"),
    path("edit/<slug:pk>/", ProjectUpdateView.as_view(), name="project_edit"),
    path("delete/<slug:pk>/", delete_project, name="project_delete")
]