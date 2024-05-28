from django.db import models
from good_recieve.models import PharmacyList
from datetime import datetime  

# Create your models here.

class owner(models.Model):
    fullname = models.CharField(max_length = 150, blank=True,default=None,null=True)
    phone = models.CharField(max_length = 11, blank=True,default=None,null=True)
    password = models.CharField(max_length = 150, blank=True,default=None,null=True)
    gender = models.CharField(max_length = 10, blank=True,default=None,null=True)
    nid = models.CharField(max_length = 50, blank=True,default=None,null=True)
    center = models.CharField(max_length = 100, blank=True,default=None,null=True)
    role = models.CharField(max_length = 500, blank=True,default=None,null=True)
    outlet = models.CharField(max_length = 500, blank=True,default=None,null=True)
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    active = models.CharField(max_length = 3, blank=True,default=None,null=True)
    shift_start = models.CharField(max_length = 15, blank=True,default=None,null=True)
    shift_end = models.CharField(max_length = 15, blank=True,default=None,null=True)

    class Meta:
        ordering = ('id',)

class otp_table(models.Model):
    owner_id = models.ForeignKey(owner , on_delete=models.CASCADE,)
    outlet_id = models.CharField(max_length = 10, blank=True,default=None,null=True)
    otp = models.CharField(max_length = 10, blank=True,default=None,null=True)
    

    class Meta:
        ordering = ('id',)
