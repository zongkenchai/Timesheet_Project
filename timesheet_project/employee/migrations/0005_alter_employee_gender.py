# Generated by Django 4.2.8 on 2023-12-16 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0004_employee_fk_position_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
                default="Male",
                max_length=10,
            ),
        ),
    ]
