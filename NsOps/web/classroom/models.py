from __future__ import unicode_literals

from django.db import models
# Create your models here.
class Company(models.Model):
    full_name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    tel = models.CharField(max_length=15,blank=True)
class Product(models.Model):
    product_name = models.CharField(max_length=30)
    price = models.FloatField()
    stock = models.IntegerField(max_length=5)
    company = models.ForeignKey(Company)
# Create your models here.
