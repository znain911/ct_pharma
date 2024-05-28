# Generated by Django 5.0.2 on 2024-03-24 08:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("good_recieve", "0004_medlist_buying_price_medlist_selling_price"),
    ]

    operations = [
        migrations.CreateModel(
            name="PharmacyList",
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
                    "outlet",
                    models.CharField(
                        blank=True, default=None, max_length=100, null=True
                    ),
                ),
                (
                    "shortCode",
                    models.SmallIntegerField(blank=True, default=None, null=True),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
    ]