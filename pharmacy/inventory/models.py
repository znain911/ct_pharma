from django.db import models
from datetime import datetime  
from good_recieve.models import CompanyList , OrderList ,PharmacyList

class InventoryList(models.Model):
    company_id = models.ForeignKey(CompanyList , on_delete=models.CASCADE,)
    req_id = models.ForeignKey(OrderList , on_delete=models.CASCADE,default=None,null=True)
    pr_id = models.BigIntegerField( blank=True,default=None,null=True)
    po_id = models.BigIntegerField( blank=True,default=None,null=True)
    purchase_id = models.CharField( max_length = 50, blank=True,default=None,null=True)
    amount = models.CharField(max_length = 100, blank=True,default=None,null=True)
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField( max_length = 100,blank=True,default=None,null=True)
    outlet_id = models.ForeignKey( PharmacyList , on_delete=models.CASCADE,default=None,null=True)
    outlet_shortcode = models.CharField( max_length = 20,blank=True,default=None,null=True)
    voucher = models.CharField( max_length = 50,blank=True,default=None,null=True)
    receive_by = models.CharField( max_length = 20,blank=True,default=None,null=True)

    class Meta:
        ordering = ('id',)

class InventoryMed(models.Model):
    med_name = models.CharField(max_length = 100, blank=True,default=None,null=True)
    company_id = models.ForeignKey(CompanyList , on_delete=models.CASCADE,)
    inventory_id = models.ForeignKey(InventoryList , on_delete=models.CASCADE,)
    req_id = models.ForeignKey(OrderList , on_delete=models.CASCADE,)
    quantity = models.CharField(max_length = 50, blank=True,default=None,null=True)
    quantity_stock = models.CharField(max_length = 150, blank=True,default=None,null=True)
    quantity_sold = models.CharField(max_length = 150, blank=True,default=None,null=True)
    status = models.CharField(max_length = 2, blank=True,default=None,null=True)
    buying_price = models.CharField(max_length = 20, blank=True,default=None,null=True)
    selling_price = models.CharField(max_length = 20, blank=True,default=None,null=True)
    total = models.CharField(max_length = 20, blank=True,default=None,null=True)
    vat_percentage = models.CharField(max_length = 20, blank=True,default=None,null=True)
    total_vat = models.CharField(max_length = 150, blank=True,default=None,null=True)
    total_vat_mrp = models.CharField(max_length = 150, blank=True,default=None,null=True)
    expired_date = models.CharField(max_length = 50, blank=True,default=None,null=True)
    generic = models.CharField(max_length = 50, blank=True,default=None,null=True)
    unit = models.CharField(max_length = 50, blank=True,default=None,null=True)


    class Meta:
        ordering = ('id',)

class stockTransferList(models.Model):
    company_id = models.ForeignKey(CompanyList , on_delete=models.CASCADE,)
    inventory_id = models.ForeignKey(InventoryList , on_delete=models.CASCADE,)
    to_outlet_id = models.CharField(max_length = 50, blank=True,default=None,null=True)
    purchase_id = models.CharField( max_length = 50, blank=True,default=None,null=True)
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField( max_length = 100,blank=True,default=None,null=True)
    from_outlet_id = models.CharField( max_length = 50, blank=True,default=None,null=True)
    outlet_shortcode = models.CharField( max_length = 20,blank=True,default=None,null=True)
    voucher = models.CharField( max_length = 50,blank=True,default=None,null=True)
    receive_by = models.CharField( max_length = 20,blank=True,default=None,null=True)

    class Meta:
        ordering = ('id',)

class stockTransferMed(models.Model):
    med_name = models.CharField(max_length = 100, blank=True,default=None,null=True)
    company_id = models.ForeignKey(CompanyList , on_delete=models.CASCADE,)
    transfer_id = models.ForeignKey(stockTransferList , on_delete=models.CASCADE,)
    quantity = models.CharField(max_length = 50, blank=True,default=None,null=True)
    quantity_stock = models.CharField(max_length = 150, blank=True,default=None,null=True)
    quantity_sold = models.CharField(max_length = 150, blank=True,default=None,null=True)
    status = models.CharField(max_length = 2, blank=True,default=None,null=True)
    buying_price = models.CharField(max_length = 20, blank=True,default=None,null=True)
    selling_price = models.CharField(max_length = 20, blank=True,default=None,null=True)
    total = models.CharField(max_length = 20, blank=True,default=None,null=True)
    vat_percentage = models.CharField(max_length = 20, blank=True,default=None,null=True)
    total_vat = models.CharField(max_length = 150, blank=True,default=None,null=True)
    total_vat_mrp = models.CharField(max_length = 150, blank=True,default=None,null=True)
    expired_date = models.CharField(max_length = 50, blank=True,default=None,null=True)
    generic = models.CharField(max_length = 50, blank=True,default=None,null=True)
    unit = models.CharField(max_length = 50, blank=True,default=None,null=True)
    outlet_id = models.CharField(max_length = 50, blank=True,default=None,null=True)

    class Meta:
        ordering = ('id',)



# Create your models here.
