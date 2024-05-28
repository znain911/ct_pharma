from django.db import models
from datetime import datetime  
from login.models import owner

# Create your models here.

class customers(models.Model):
    name = models.CharField(max_length = 100, blank=True,default=None,null=True)
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    register_by = models.ForeignKey(owner , on_delete=models.CASCADE,)
