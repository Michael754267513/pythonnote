# -*- coding: utf8 -*-
from django.db import models

# Create your models here.


class Repository(models.Model):
    REPO_TYPE_CHOICE = (
        (u'1', u'git'),
        (u'2', u'svn'),
    )

    REPO_PROTOCOL_CHOICE = (
        (u'1', u'ssh'),
        (u'2', u'http'),
        (u'3', u'https'),
    )

    repo_name = models.CharField(max_length=20, verbose_name=u'仓库名')
    repo_address = models.CharField(max_length=200, verbose_name=u'仓库地址')
    repo_user = models.CharField(max_length=50, verbose_name=u'仓库用户名')
    repo_pass = models.CharField(max_length=20, verbose_name=u'仓库用户密码', blank=True, null=True)
    repo_type = models.CharField(max_length=1, verbose_name=u'仓库类型', choices=REPO_TYPE_CHOICE)
    repo_protocol = models.CharField(max_length=1, verbose_name=u'使用协议', choices=REPO_PROTOCOL_CHOICE)
    repo_tag = models.CharField(max_length=20, verbose_name=u'仓库标识')

    class Meta:
        permissions = (
            ('view_repository', 'Can view repository'),
        )

    def __unicode__(self):
        return self.repo_name


class Version(models.Model):

    VERSION_STATIC_CHOICE = (
        (u'0', u'disable'),
        (u'1', u'release'),
        (u'2', u'backup'),
        (u'3', u'rollback'),
    )

    project = models.CharField(max_length=20, verbose_name=u'项目名', blank=True)
    version = models.CharField(max_length=20, verbose_name=u'版本号', unique=True)
    timestamp = models.DateTimeField(verbose_name=u'时间')
    author = models.CharField(max_length=20, verbose_name=u'提交用户')
    vernier = models.CharField(max_length=1, verbose_name=u'游标', choices=VERSION_STATIC_CHOICE)
    content = models.TextField(verbose_name=u'备注')

    class Meta:
        permissions = (
            ('view_version', 'Can view repo version'),
        )

    def __unicode__(self):
        return '%s | %s' % (self.project, self.version)
