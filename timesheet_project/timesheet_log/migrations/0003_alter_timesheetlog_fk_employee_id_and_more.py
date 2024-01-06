# Generated by Django 4.2.8 on 2024-01-06 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0006_alter_employee_fk_position_id"),
        ("project", "0004_alter_project_expected_revenue"),
        ("timesheet_log", "0002_timesheetlog_date_timesheetlog_duration_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="timesheetlog",
            name="fk_employee_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="employee.employee"
            ),
        ),
        migrations.AlterField(
            model_name="timesheetlog",
            name="fk_project_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="project.project"
            ),
        ),
    ]
