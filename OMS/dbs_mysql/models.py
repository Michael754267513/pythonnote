# -*- coding:utf8 -*-
from django.db import models
from s.models import
from oms_config.models import Zone


# Create your models here.


class Databases(models.Model):
    s = models.ForeignKey(, on_delete=models.CASCADE, verbose_name=u'业务组')
    schema = models.CharField(max_length=20, verbose_name=u'实例名', unique=True)
    alias_name = models.CharField(max_length=20, verbose_name=u'别名')
    ip_address = models.IPAddressField(max_length=15, verbose_name=u'数据库地址')
    port = models.IntegerField(verbose_name=u'数据库端口', default=3306)
    schema_user = models.CharField(max_length=20, verbose_name=u'实例管理员')
    schema_pass = models.CharField(max_length=20, verbose_name=u'实例管理员密码')
    zones = models.ManyToManyField(Zone, verbose_name=u'游戏分区')

    class Meta:
        permissions = (
            ('view_databases', 'Can view Databases'),
        )

    def __unicode__(self):
        return '%s %s' % (self.schema, self.ip_address)


# class DBAccounts(models.Model):
#     databases = models.ForeignKey(Databases, on_delete=models.CASCADE, verbose_name=u'数据库')
#     username = models.CharField(max_length=20, verbose_name=u'用户名')
#     hosts = models.CharField(max_length=50, verbose_name=u'主机')
#     create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
#     edit_time = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
#     content = models.TextField(verbose_name=u'备注', blank=None, null=True)
#
#     class Meta:
#         permissions = (
#             ('view_dbaccounts', 'can view mysql accounts'),
#         )
#