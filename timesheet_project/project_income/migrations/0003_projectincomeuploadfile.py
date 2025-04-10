# Generated by Django 4.2.8 on 2024-01-06 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project_income", "0002_alter_projectincome_amount_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectIncomeUploadFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("file", models.FileField(upload_to="uploads/project_income/")),
            ],
        ),
    ]
