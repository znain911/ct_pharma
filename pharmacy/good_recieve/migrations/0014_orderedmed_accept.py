# Generated by Django 5.0.2 on 2024-04-03 05:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("good_recieve", "0013_medlist_generic_orderedmed"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderedmed",
            name="accept",
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
