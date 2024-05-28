# Generated by Django 5.0.2 on 2024-04-04 07:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("good_recieve", "0014_orderedmed_accept"),
        ("inventory", "0002_inventorylist_req_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="inventorylist",
            name="outlet_id",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="good_recieve.pharmacylist",
            ),
        ),
    ]
