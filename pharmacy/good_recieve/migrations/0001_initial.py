# Generated by Django 5.0.2 on 2024-03-18 06:13

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CompanyList",
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
                (
                    "companyName",
                    models.CharField(blank=True, default=None, max_length=100),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
    ]
