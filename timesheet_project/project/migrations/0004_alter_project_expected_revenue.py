# Generated by Django 4.2.8 on 2024-01-06 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0003_alter_project_fk_company_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="expected_revenue",
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
    ]
