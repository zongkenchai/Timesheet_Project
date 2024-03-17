from django.urls import path
from .views import *


urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("create/", ProjectCreateView.as_view(), name="project_create"),
    path("edit/<slug:pk>/", ProjectUpdateView.as_view(), name="project_edit"),
    path("delete/<slug:pk>/", delete_project, name="project_delete"),
    path("detail/<slug:pk>/", ProjectDetailView.as_view(), name='project_detail'),
    path("target-revenue/create/<int:project_id>", ProjectTargetRevenueCreateView.as_view(), name='project_target_revenue_create'),
    path("target-revenue/edit/<slug:pk>/<int:project_id>/", ProjectTargetRevenueUpdateView.as_view(), name='project_target_revenue_edit'),
    path("target-revenue/delete/<slug:pk>/<int:project_id>/", delete_project_target_revenue, name='project_target_revenue_delete'),
]