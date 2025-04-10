# Generated by Django 4.2.8 on 2024-01-05 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0001_initial"),
        ("project", "0002_project_fk_company_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="fk_company_name",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="company.company"
            ),
        ),
    ]
