# Generated by Django 5.0.2 on 2024-03-25 06:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("good_recieve", "0005_pharmacylist"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderList",
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
                ("pr_id", models.BigIntegerField(blank=True, default=None, null=True)),
                ("po_id", models.BigIntegerField(blank=True, default=None, null=True)),
                (
                    "purchase_id",
                    models.BigIntegerField(blank=True, default=None, null=True),
                ),
                (
                    "amount",
                    models.CharField(
                        blank=True, default=None, max_length=100, null=True
                    ),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                (
                    "company_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="good_recieve.companylist",
                    ),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
    ]