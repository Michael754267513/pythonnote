# -*- coding:utf8 -*-

from django.db import models
from s.models import

# Create your models here.


class Redis(models.Model):
    SPEC_CHOICE = (
        (u'1', u'单机'),
        (u'2', u'主从'),
        (u'3', u'集群'),
    )

    schema = models.CharField(max_length=50, verbose_name=u'实例名称', unique=True)
    ip_address = models.IPAddressField(max_length=15, verbose_name=u'数据库地址')
    s = models.ForeignKey(, verbose_name=u'所属项目组')
    status = models.BooleanField(verbose_name=u'实例状态', default=False)
    spec = models.CharField(max_length=1, verbose_name=u'规格', choices=SPEC_CHOICE)
    port = models.IntegerField(verbose_name=u'端口', default=6379)
    password = models.CharField(max_length=20, verbose_name=u'redis密码', blank=True, null=True)

    class Meta:
        permissions = (
            ('view_redis', 'Can view redis'),
        )

    def __unicode__(self):
        return self.schema

