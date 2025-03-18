from django.urls import path
from .views import *


urlpatterns = [
    path("", PositionListView.as_view(), name="position_list"),
    path("create/", PositionCreateView.as_view(), name="position_create"),
    path("edit/<slug:pk>/", PositionUpdateView.as_view(), name="position_edit"),
    path("delete/<slug:pk>/", delete_position, name="position_delete")
]