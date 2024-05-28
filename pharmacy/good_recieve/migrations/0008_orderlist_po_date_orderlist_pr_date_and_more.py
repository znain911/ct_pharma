# Generated by Django 5.0.2 on 2024-03-25 07:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("good_recieve", "0007_alter_orderlist_create_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderlist",
            name="po_date",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="orderlist",
            name="pr_date",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="orderlist",
            name="purchase_date",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="orderlist",
            name="status",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]