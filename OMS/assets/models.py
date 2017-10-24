# --*-- coding: utf-8 --*--

from django.db import models
from s.models import
from oms_config.models import Zone

# Create your models here.


class Hardware(models.Model):
    UNIT_CHOICES = (
        (u'1', u'GB'),
        (u'2', u'Core'),
    )

    name = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'硬件名')
    value = models.IntegerField(blank=True, null=True, verbose_name=u'硬件值')
    unit = models.CharField(max_length=10, blank=True, null=True, choices=UNIT_CHOICES, verbose_name=u'单位')

    class Meta:
        permissions = (
            ('view_hardware', 'Can view Hardware'),
        )

    def __unicode__(self):
        return '%s %s %s' % (self.name, self.value, self.get_unit_display())


class Network(models.Model):
    NET_TYPE_CHOICES = (
        (u'1', u'BGP'),
        (u'2', u'电信'),
        (u'3', u'联通'),
        (u'4', u'移动'),
        (u'5', u'教育'),
        (u'6', u'内网'),
    )

    UNIT_CHOICES = (
        (u'1', u'Mbps'),
    )

    public_address = models.IPAddressField(blank=True, null=True, verbose_name=u'公网地址')
    private_address = models.IPAddressField(blank=True, null=True, verbose_name=u'内网地址')
    bandwidth = models.IntegerField(blank=True, null=True, verbose_name=u'带宽')
    provide = models.CharField(max_length=20, verbose_name=u'接入商', blank=True, null=True)
    net_type = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'网络类型', choices=NET_TYPE_CHOICES)
    unit = models.CharField(max_length=10, blank=True, null=True, verbose_name=u'单位', choices=UNIT_CHOICES)
    bind = models.BooleanField(default=False, verbose_name=u'绑定', blank=True)

    class Meta:
        permissions = (
            ('view_network', 'Can view network'),
        )

    def __unicode__(self):
        return '%s %s %s %s %s %s' % (self.public_address, self.private_address, self.provide,
                                      self.net_type, self.bandwidth, self.get_unit_display())


class Services(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'服务名')
    port = models.IntegerField(verbose_name=u'端口', blank=True, null=True)

    class Meta:
        permissions = (
            ('view_service', 'can view services'),
        )

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'标签名', blank=True, null=True, unique=True)

    class Meta:
        permissions = (
            ('view_tag', 'Can view tags'),
        )

    def __unicode__(self):
        return self.name


class Assets(models.Model):
    HOST_TYPE_CHOICES = (
        (u'1', u'物理机'),
        (u'2', u'云主机'),
        (u'3', u'虚拟机'),
    )

    OS_CHOICES = (
        (u'1', u'CentOS 7.2 X86 64bit'),
        (u'2', u'CentOS 7.0 x86 64bit'),
    )

    host_name = models.CharField(max_length=50, verbose_name=u'主机名', unique=True)
    alias_name = models.CharField(max_length=100, verbose_name=u'可见名', blank=True, null=True)
    host_type = models.CharField(max_length=10, blank=True, null=True,
                                 choices=HOST_TYPE_CHOICES, verbose_name=u'主机类型')
    tag = models.ManyToManyField(Tag, verbose_name=u'标识')
    game_zone = models.ManyToManyField(Zone, verbose_name=u'游戏区')
    os = models.CharField(max_length=10, blank=True, null=True,
                          choices=OS_CHOICES, verbose_name=u'操作系统')
    superuser = models.CharField(max_length=20, verbose_name=u'管理员', default=u'root')
    superuser_pass = models.CharField(max_length=50, verbose_name=u'管理员密码', blank=True, null=True)
    is_online = models.BooleanField(blank=True, default=False, verbose_name=u'在线')
    is_unused = models.BooleanField(verbose_name=u'闲置', default=False)
    is_master = models.BooleanField(blank=True, default=False, verbose_name=u'salt-master')
    is_minion = models.BooleanField(blank=True, default=False, verbose_name=u'salt-minion')
    hardware = models.ManyToManyField(Hardware, verbose_name=u'硬件配置')
    networks = models.OneToOneField(Network, on_delete=models.CASCADE, verbose_name=u'网络', related_name='assets')
    s = models.ForeignKey(, on_delete=models.CASCADE, verbose_name=u'业务组', blank=True, null=True)
    services = models.ManyToManyField(Services, verbose_name=u'运行的服务')

    class Meta:
        permissions = (
            ('view_assets', 'Can view assets'),
        )

    def __unicode__(self):
        return self.alias_name


class SysUser(models.Model):
    servers = models.ForeignKey(Assets, verbose_name=u'服务器')
    sys_user = models.CharField(max_length=50, verbose_name=u'用户', blank=True, null=True)
    sys_pass = models.CharField(max_length=200, verbose_name=u'密码', blank=True, null=True)

    class Meta:
        permissions = (
            ('view_sysuser', 'can view sys user information'),
        )

    def __unicode__(self):
        return '%s %s' % (self.sys_user, self.sys_pass)
