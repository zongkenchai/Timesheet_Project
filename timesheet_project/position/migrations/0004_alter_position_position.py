# Generated by Django 4.2.8 on 2024-03-22 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("position", "0003_remove_position_department"),
    ]

    operations = [
        migrations.AlterField(
            model_name="position",
            name="position",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
