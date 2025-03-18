from django.urls import path
from .views import *

urlpatterns = [
    path("", TimesheetLogListView.as_view(), name="timesheet_log_list"),
    path("create/", TimesheetLogCreateView.as_view(), name="timesheet_log_create"),
    path("edit/<slug:pk>/", TimesheetLogUpdateView.as_view(), name="timesheet_log_edit"),
    path("delete/<slug:pk>/", delete_timesheet_log, name="timesheet_log_delete")
]