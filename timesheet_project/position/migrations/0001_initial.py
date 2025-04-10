# Generated by Django 4.2.8 on 2023-12-16 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Position",
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
                ("title", models.CharField(max_length=50)),
                (
                    "department",
                    models.CharField(
                        choices=[
                            ("Technical", "Technical"),
                            ("Finance", "Finance"),
                            ("HR", "HR"),
                        ],
                        default="Technical",
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]
