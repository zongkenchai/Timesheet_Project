from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)