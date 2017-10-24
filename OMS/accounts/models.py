from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=32, blank=True, null=True)
    home = models.CharField(max_length=32, blank=True, null=True)
    job = models.CharField(max_length=32, blank=True, null=True)

    def __unicode__(self):
        return self.username
