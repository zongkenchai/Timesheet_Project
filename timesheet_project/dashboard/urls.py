from django.urls import path
from .views import *


urlpatterns = [
    path("", DashboardView.as_view(), name='dashboard'),
    path("update/", update_dashboard, name='update_dashboard')
]