# --*-- coding:utf-8 --*--

from django.db import models

# Create your models here.


class (models.Model):
    name = models.CharField(max_length=50, verbose_name=u"业务组", unique=True)
    tag = models.CharField(max_length=20, verbose_name=u'业务组标记', unique=True)

    class Meta:
        permissions = (
            ('view_', 'can view '),
        )

    def __unicode__(self):
        return self.name
