
from django.contrib import admin

# from .models import NewUser
from .models import RegisteredEmail

# Register your models here.
# admin.site.register(NewUser)
admin.site.register(RegisteredEmail)
# admin.site.register(User)

# pg_dump -U django_admin -h 5433 -d timesheet_project > backup.sql
# pg_dump -U django_admin -h localhost -p 5433 -d timesheet_project > backup.sql
