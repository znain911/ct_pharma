# Generated by Django 5.0.2 on 2024-04-04 07:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("good_recieve", "0014_orderedmed_accept"),
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="inventorylist",
            name="req_id",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="good_recieve.orderlist",
            ),
        ),
    ]
