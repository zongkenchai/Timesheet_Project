from django.urls import path
from .views import *

urlpatterns = [
	path('', RegistrationView.as_view(), name='register_email'),
	path('edit/<slug:pk>', RegisterEmailUpdateView.as_view(),name='register_edit'),
	path('create/', RegisterEmailCreateView.as_view(), name='give_email_permission'), 
	path('delete/<str:id>',delete_row,name='register_delete'),
]