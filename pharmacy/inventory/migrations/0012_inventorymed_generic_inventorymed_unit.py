# Generated by Django 5.0.2 on 2024-05-05 10:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0011_inventorylist_voucher"),
    ]

    operations = [
        migrations.AddField(
            model_name="inventorymed",
            name="generic",
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="inventorymed",
            name="unit",
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
