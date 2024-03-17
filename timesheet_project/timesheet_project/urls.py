"""
URL configuration for timesheet_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('company/', include('company.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('employee/', include('employee.urls')),
    path('payroll/', include('payroll.urls')),
    path('position/', include('position.urls')),
    path('project/', include('project.urls')),
    path('project_income/', include('project_income.urls')),
    path('timesheet_log/', include('timesheet_log.urls')),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', include('customauth.urls')),
    path('register-email/', include('user_registration.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
