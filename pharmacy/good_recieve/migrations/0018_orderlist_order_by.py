# Generated by Django 5.0.2 on 2024-05-07 11:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("good_recieve", "0017_med_unit"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderlist",
            name="order_by",
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
