# -*- coding:utf8 -*-

from django.db import models
from s.models import


# Create your models here.


class Zone(models.Model):
    s = models.ForeignKey(, on_delete=models.CASCADE, verbose_name=u'业务组')
    name = models.CharField(max_length=50, verbose_name=u'游戏分区', unique=True)
    content = models.CharField(max_length=200, verbose_name=u'备注', blank=True, null=True)

    class Meta:
        permissions = (
            ('view_zone', 'Can view game zone'),
        )

    def __unicode__(self):
        return self.name


class Information(models.Model):
    zones = models.ForeignKey(Zone, on_delete=models.CASCADE,
                              verbose_name=u'游戏分区', blank=True, null=True)
    key = models.CharField(max_length=50, verbose_name=u'字段名')
    value = models.CharField(max_length=200, verbose_name=u'字段值')
    timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)
    context = models.CharField(max_length=200, verbose_name=u'备注', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_information', 'Can view information'),
        )

    def __unicode__(self):
        return '%s %s' % (self.name, self.value)


class Upload(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name=u'标题')
    doc_file = models.FileField(upload_to='Upload')
    timestamp = models.DateTimeField(verbose_name=u'上传时间', auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_upload', 'can view upload file'),
        )

    def __unicode__(self):
        return '%s' % self.doc_file

    def display_text_file(self):
        with open(self.doc_file.path) as fp:
            return fp.read()


class Path(models.Model):
    s = models.ForeignKey(, on_delete=models.CASCADE, verbose_name=u'业务组')
    path_key = models.CharField(max_length=100, verbose_name=u'路径名', unique=True)
    path_value = models.CharField(max_length=2000, verbose_name=u'路径值')
    timestamp = models.DateTimeField(verbose_name=u'时间', auto_now=True)

    class Meta:
        permissions = (
            ('view_path', 'can view path'),
        )

    def __unicode__(self):
        return self.path_value


class Produce(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组', on_delete=models.CASCADE)
    zones = models.ManyToManyField(Zone, verbose_name=u"游戏分区")
    config_file = models.CharField(max_length=200, verbose_name=u'配置文件')
    generate_path = models.CharField(max_length=200, verbose_name=u'生成路径')
    project_name = models.CharField(max_length=50, verbose_name=u'对应仓库项目')
    create_time = models.DateTimeField(verbose_name=u'生成时间', auto_now=True)

    class Meta:
        ordering = ['-create_time']
        permissions = (
            ('view_produce', 'Can view produce'),
        )

    def __unicode__(self):
        return self.generate_path


class Domain(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组', on_delete=models.CASCADE)
    zones = models.ForeignKey(Zone, verbose_name=u'游戏分区', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name=u'域名')
    timestamp = models.DateField(verbose_name=u'时间', auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_domain', 'Can view Domain'),
        )

    def __unicode__(self):
        return '%s | %s' % (self.zones, self.name)
