from django.db import models
from datetime import datetime  

# Create your models here.

class CompanyList(models.Model):
    companyName = models.CharField(max_length = 100, blank=True,default=None,null=True)
    shortCode = models.CharField(max_length = 10, blank=True,default=None,null=True)

    class Meta:
        ordering = ('id',)

class PharmacyList(models.Model):
    outlet = models.CharField(max_length = 100, blank=True,default=None,null=True)
    shortCode = models.SmallIntegerField( blank=True,default=None,null=True)

    class Meta:
        ordering = ('id',)

class MedList(models.Model):
    med_name = models.CharField(max_length = 100, blank=True,default=None,null=True)
    company_id = models.ForeignKey(CompanyList , on_delete=models.CASCADE,)
    generic = models.CharField(max_length = 100, blank=True,default=None,null=True)
    buying_price = models.CharField(max_length = 20, blank=True,default=None,null=True)
    selling_price = models.CharField(max_length = 20, blank=True,default=None,null=True)

    class Meta:
        ordering = ('id',)

class OrderList(models.Model):
    company_id = models.ForeignKey(CompanyList , on_delete=models.CASCADE,)
    pr_id = models.CharField( max_length = 50,blank=True,default=None,null=True)
    pr_date = models.CharField( max_length = 50,blank=True,default=None,null=True)
    po_id = models.BigIntegerField( blank=True,default=None,null=True)
    po_date = models.CharField( max_length = 100,blank=True,default=None,null=True)
    purchase_id = models.BigIntegerField( blank=True,default=None,null=True)
    purchase_date = models.CharField( max_length = 100,blank=True,default=None,null=True)
    amount = models.CharField(max_length = 100, blank=True,default=None,null=True)
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField( max_length = 100,blank=True,default=None,null=True)
    outlet_id = models.CharField( max_length = 20,blank=True,default=None,null=True)
    outlet_shortcode = models.CharField( max_length = 20,blank=True,default=None,null=True)
    order_by = models.CharField( max_length = 20,blank=True,default=None,null=True)

    class Meta:
        ordering = ('id',)


class OrderedMed(models.Model):
    med_name = models.CharField(max_length = 100, blank=True,default=None,null=True)
    company_id = models.ForeignKey(CompanyList , on_delete=models.CASCADE,)
    order_id = models.ForeignKey(OrderList , on_delete=models.CASCADE,)
    quantity = models.CharField(max_length = 50, blank=True,default=None,null=True)
    generic = models.CharField(max_length = 50, blank=True,default=None,null=True)
    unit = models.CharField(max_length = 50, blank=True,default=None,null=True)
    buying_price = models.CharField(max_length = 20, blank=True,default=None,null=True)
    selling_price = models.CharField(max_length = 20, blank=True,default=None,null=True)
    accept = models.CharField(max_length = 50, blank=True,default=None,null=True)

    class Meta:
        ordering = ('id',)

class med_unit(models.Model):
    unit = models.CharField(max_length = 50, blank=True,default=None,null=True)

    class Meta:
        ordering = ('id',)

class generic_list(models.Model):
    name = models.CharField(max_length = 100, blank=True,default=None,null=True)

    class Meta:
        ordering = ('id',)