# Generated by Django 4.2.8 on 2024-03-22 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("project_income", "0007_projectinvoice_projectinvoiceuploadfile_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectpayment",
            name="fk_invoice_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="project_income.projectinvoice",
            ),
        ),
    ]
