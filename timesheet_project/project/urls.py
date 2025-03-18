from django.urls import path
from .views import *


urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("create/", ProjectCreateView.as_view(), name="project_create"),
    path("edit/<slug:pk>/", ProjectUpdateView.as_view(), name="project_edit"),
    path("delete/<slug:pk>/", delete_project, name="project_delete"),
    path("detail/<slug:pk>/", ProjectDetailView.as_view(), name='project_detail'),
    path("phase/create/<int:project_id>/", ProjectPhaseCreateView.as_view(), name='project_phase_create'),
    path("phase/edit/<slug:pk>/<int:project_id>/", ProjectPhaseUpdateView.as_view(), name='project_phase_edit'),
    path("phase/detail/<slug:pk>/", ProjectPhaseDetailView.as_view(), name='project_phase_detail'),
    path("phase/delete/<slug:pk>/<int:project_id>/", delete_project_phase, name='project_phase_delete'),
    path("phase/target-revenue/create/<int:phase_id>", ProjectPhaseForecastRevenueCreateView.as_view(), name='project_phase_forecast_revenue_create'),
    path("phase/target-revenue/edit/<slug:pk>/<int:phase_id>/", ProjectPhaseForecastRevenueUpdateView.as_view(), name='project_phase_forecast_revenue_edit'),
    path("phase/target-revenue/delete/<slug:pk>/<int:phase_id>/", delete_project_phase_forecast_revenue, name='project_phase_forecast_revenue_delete'),
]