# Generated by Django 4.2.8 on 2024-03-22 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("timesheet_log", "0003_alter_timesheetlog_fk_employee_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="timesheetlog",
            name="duration",
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
    ]
