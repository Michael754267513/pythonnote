# -*- coding:utf-8 -*-

from django.db import models
from repository.models import Repository
from assets.models import Assets, Services
from oms_config.models import Zone, Path, Domain
from s.models import
from repository.models import Version

# Create your models here.


RELEASE_FUN_CHOICES = (
        (u'1', u'git.clone'),
        (u'2', u'git.pull'),
    )


class SaltKey(models.Model):
    MINION_TYPE = (
        (u'1', u'master'),
        (u'2', u'minion')
    )

    STATUS_CHOICES = (
        (u'1', u'accept'),
        (u'2', u'delete'),
        (u'3', u'rejected'),
    )

    minion = models.CharField(max_length=50, verbose_name=u'minions')
    type = models.CharField(max_length=1, verbose_name=u'类型', choices=MINION_TYPE)
    finger = models.CharField(max_length=200, verbose_name=u'指纹')
    timestamp = models.DateField(verbose_name=u'操作时间', auto_now=True, blank=True)
    status = models.IntegerField(default=0, verbose_name=u'状态', choices=STATUS_CHOICES)
    is_getinfo = models.BooleanField(default=False, verbose_name=u'获取信息状态')
    is_push_scripts = models.BooleanField(default=False, verbose_name=u'推送脚本状态')


class Release(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组')
    zones = models.ForeignKey(Zone, verbose_name=u'游戏分区')
    # versions = models.ForeignKey(Version, verbose_name=u'版本', blank=True, null=True)
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    client = models.CharField(max_length=20, verbose_name=u'发送指令主机', default=u'local')
    use_zone = models.BooleanField(verbose_name=u'路径使用_分区名拼接', default=False)
    tgt = models.ManyToManyField(Assets, verbose_name=u'目标主机')
    fun = models.CharField(max_length=20, verbose_name=u'执行模块', choices=RELEASE_FUN_CHOICES)
    deploy_path = models.CharField(verbose_name=u'部署路径', max_length=200)
    release_path = models.CharField(verbose_name=u'发布路径', max_length=200, blank=True, null=True)
    repository_name = models.ForeignKey(Repository, verbose_name=u'仓库名')
    status = models.BooleanField(default=False, verbose_name=u'执行结果状态')
    content = models.TextField(max_length=200, verbose_name=u'更新说明')
    context = models.TextField(max_length=2000, verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_release', 'Can view code release'),
        )


class Backup(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组')
    zones = models.ForeignKey(Zone, verbose_name=u'游戏分区')
    # versions = models.ForeignKey(Version, verbose_name=u'版本')
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    client = models.CharField(max_length=20, verbose_name=u'发送指令主机', default=u'local')
    use_zone = models.BooleanField(verbose_name=u'路径使用_分区名拼接', default=False)
    tgt = models.ManyToManyField(Assets, verbose_name=u'目标主机')
    fun = models.CharField(max_length=20, verbose_name=u'执行模块', default='cmd.run')
    deploy_path = models.CharField(verbose_name=u'部署路径', max_length=200)
    backup_path = models.CharField(verbose_name=u'备份目录', max_length=200, blank=True, null=True)
    repository_name = models.ForeignKey(Repository, verbose_name=u'仓库名')
    status = models.BooleanField(default=False, verbose_name=u'执行结果状态')
    content = models.TextField(max_length=200, verbose_name=u'更新说明')
    context = models.TextField(max_length=2000, verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_backup', 'Can view code backup'),
        )

    def __unicode__(self):
        return self.backup_path


class RollBack(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组')
    zones = models.ForeignKey(Zone, verbose_name=u'游戏分区')
    # versions = models.ForeignKey(Version, verbose_name=u'版本')
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    client = models.CharField(max_length=20, verbose_name=u'发送指令主机', default=u'local')
    use_zone = models.BooleanField(verbose_name=u'路径使用_分区名拼接', default=False)
    tgt = models.ManyToManyField(Assets, verbose_name=u'目标主机')
    fun = models.CharField(max_length=20, verbose_name=u'执行模块', default='cmd.run')
    rollback_package = models.CharField(verbose_name=u'回档包', max_length=200, blank=True, null=True)
    repository_name = models.ForeignKey(Repository, verbose_name=u'仓库名')
    status = models.BooleanField(default=False, verbose_name=u'执行结果状态')
    content = models.TextField(max_length=200, verbose_name=u'更新说明')
    context = models.TextField(max_length=2000, verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_rollback', 'Can view code rollback'),
        )


class Push(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组')
    zones = models.ForeignKey(Zone, verbose_name=u'游戏分区')
    domains = models.ForeignKey(Domain, verbose_name=u'域名')
    service_name = models.CharField(max_length=1, verbose_name=u'服务名')
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    client = models.CharField(max_length=20, verbose_name=u'发送指令主机', default=u'local')
    tgt = models.ManyToManyField(Assets, verbose_name=u'目标主机')
    fun = models.CharField(max_length=20, verbose_name=u'执行模块', default=u'cp.get_template')
    source_path = models.CharField(max_length=100, verbose_name=u'目标路径',
                                   default=u'salt://service_config')
    target_path = models.ForeignKey(Path, verbose_name=u'目标路径')
    file_name = models.CharField(max_length=50, verbose_name=u'文件名')
    status = models.BooleanField(default=False, verbose_name=u'执行结果状态')
    context = models.TextField(max_length=2000, verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_push', 'Can view file push'),
        )


class ServicesHandle(models.Model):
    SERVICES_FUN_CHOICES = (
        (u'service.start', u'service.start'),
        (u'service.restart', u'service.restart'),
        (u'service.stop', u'service.stop'),
        (u'service.reload', u'service.reload'),
        (u'service.status', u'service.status'),
    )
    s = models.ForeignKey(, verbose_name=u'业务组')
    # zones = models.ForeignKey(Zone, verbose_name=u'游戏分区')
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    client = models.CharField(max_length=20, verbose_name=u'发送指令主机', default=u'local')
    tgt = models.ManyToManyField(Assets, verbose_name=u'目标主机')
    fun = models.CharField(max_length=50, verbose_name=u'执行模块', choices=SERVICES_FUN_CHOICES)
    services = models.ForeignKey(Services, verbose_name=u'服务名')
    status = models.BooleanField(default=False, verbose_name=u'执行结果状态')
    context = models.TextField(max_length=2000, verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_servicehandle', 'Can view service handle'),
        )


class ExecuteCommand(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组')
    # zones = models.ForeignKey(Zone, verbose_name=u'游戏分区')
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    client = models.CharField(max_length=20, verbose_name=u'发送指令主机', default=u'local')
    tgt = models.ManyToManyField(Assets, verbose_name=u'目标主机')
    fun = models.CharField(max_length=100, verbose_name=u'执行模块', default='cmd.run')
    commands = models.CharField(max_length=2000, verbose_name=u'命令')
    status = models.BooleanField(default=False, verbose_name=u'执行结果状态')
    context = models.TextField(max_length=2000, verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_execute_command', 'Can view execute command'),
        )


class Cron(models.Model):
    CRON_FUN_CHOICES = (
        (u'cron.raw_cron', u'cron.raw_cron'),
        (u'cron.set_job', u'cron.set_job'),
        (u'cron.rm_job', u'cron.rm_job'),
    )
    s = models.ForeignKey(, verbose_name=u'业务组')
    zones = models.ForeignKey(Zone, verbose_name=u'游戏分区')
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    client = models.CharField(max_length=20, verbose_name=u'发送指令主机', default=u'local')
    tgt = models.ManyToManyField(Assets, verbose_name=u'目标主机')
    fun = models.CharField(max_length=100, verbose_name=u'执行模块', choices=CRON_FUN_CHOICES)
    minute = models.CharField(max_length=10, verbose_name=u'分钟', blank=True, null=True)
    hour = models.CharField(max_length=10, verbose_name=u'时', blank=True, null=True)
    day = models.CharField(max_length=10, verbose_name=u'天', blank=True, null=True)
    month = models.CharField(max_length=10, verbose_name=u'月', blank=True, null=True)
    day_week = models.CharField(max_length=10, verbose_name=u'星期几(1-7)', blank=True, null=True )
    sys_user = models.CharField(max_length=50, verbose_name=u'执行用户', default=u'root')
    arg = models.CharField(max_length=2000, verbose_name=u'执行参数', blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name=u'执行结果状态')
    context = models.TextField(max_length=2000, verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_cron', 'Can view cron'),
        )


class Updates(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组')
    zones = models.ManyToManyField(Zone, verbose_name=u'选择分区')
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    client = models.CharField(max_length=20, verbose_name=u'发送指令主机', default=u'local')
    use_zone = models.BooleanField(verbose_name=u'是否使用"_zone"标识', default=False)
    fun = models.CharField(max_length=100, verbose_name=u'执行模块', default=u'cmd.run')
    # tgt = models.ManyToManyField(Assets, verbose_name=u'更新服务器')
    commands = models.CharField(max_length=200, verbose_name=u'更新脚本', default='sh /data/agent_scripts/upgrade_code.sh')
    repository_name = models.ForeignKey(Repository, verbose_name=u'仓库名')
    deploy_path = models.CharField(max_length=50, verbose_name=u'部署路径')
    status = models.BooleanField(default=False, verbose_name=u'执行结果状态')
    content = models.TextField(max_length=200, verbose_name=u'更新说明')
    context = models.TextField(verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_updates', 'Can view updates'),
        )


class SystemUserManager(models.Model):

    SHELL_CHOICES = (
        (u'1', u'/bin/bash'),
        (u'2', u'/bin/chsh'),
    )

    s = models.ForeignKey(, on_delete=models.CASCADE, verbose_name=u'业务组')
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    user = models.CharField(max_length=50, verbose_name=u'用户名')
    client = models.CharField(max_length=20, verbose_name=u'client', default=u'local', blank=True)
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    fun = models.CharField(max_length=50, verbose_name=u'模块', default=u'user.add')
    home = models.CharField(max_length=50, verbose_name=u'家目录', blank=True, null=True, default=u'/home')
    shell = models.CharField(max_length=20, verbose_name=u'shell', choices=SHELL_CHOICES, blank=True, null=True)
    tgt = models.ManyToManyField(Assets, verbose_name=u'目标服务器')
    status = models.BooleanField(default=False, verbose_name=u'执行结果状态')
    context = models.TextField(verbose_name=u'返回信息', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_system user manager', 'can view system user'),
        )


class Password(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组')
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    user = models.CharField(max_length=50, verbose_name=u'系统用户')
    tgt = models.ManyToManyField(Assets, verbose_name=u'目标主机')
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    client = models.CharField(max_length=20, verbose_name=u'发送指令主机', default=u'local')
    status = models.BooleanField(default=False, verbose_name=u'执行结果状态')
    context = models.TextField(verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_password', 'can view password'),
        )


class PackageInstall(models.Model):
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    yum_package_name = models.CharField(max_length=50, verbose_name=u'包名')
    fun = models.CharField(max_length=20, verbose_name=u'模块', default=u'pkg.install')
    tgt = models.ManyToManyField(Assets, verbose_name=u'目标主机')
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    client = models.CharField(max_length=20, verbose_name=u'发送指令主机', default=u'local')
    status = models.BooleanField(default=False, verbose_name=u'执行结果状态')
    context = models.TextField(verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view_packageinstall', 'can view password'),
        )


class SyncConfig(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组')
    zones = models.ForeignKey(Zone, verbose_name=u'区号')
    tgt = models.ManyToManyField(Assets, verbose_name=u'目标主机')
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    salt_url = models.CharField(max_length=50, verbose_name=u'源路径', default='salt://config')
    dest_path = models.CharField(max_length=50, verbose_name=u'目录路径')
    repository = models.ForeignKey(Repository, verbose_name=u'仓库')
    use_zone = models.BooleanField(verbose_name=u'路径使用_分区名拼接', default=False)
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    status = models.BooleanField(default=False, verbose_name=u'状态')
    context = models.TextField(verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view syncconfig', 'can view syncconfig'),
        )


class MergeServers(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组')
    merge_zones = models.ManyToManyField(Zone, verbose_name=u'选择合并分区')
    merge_path = models.CharField(max_length=200, verbose_name=u'合并配置目录', default=u'/srv/salt/merge_config')
    # repository = models.ForeignKey(Repository, verbose_name=u'仓库')
    chat_server = models.CharField(max_length=50, verbose_name=u'聊天服务器')
    data_server = models.CharField(max_length=50, verbose_name=u'数据服')
    tgt = models.ManyToManyField(Assets, verbose_name=u'选择目标服务器')
    operate = models.CharField(verbose_name=u'操作用户', max_length=20)
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    status = models.BooleanField(verbose_name=u'状态', default=False)
    context = models.TextField(verbose_name=u'执行结果', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view merge servers', 'Can view merge Server config'),
        )


class DeployWizard(models.Model):
    s = models.ForeignKey(, verbose_name=u'业务组')
    zones = models.ForeignKey(Zone, verbose_name=u'部署分区')
    operate = models.CharField(max_length=20, verbose_name=u'操作用户')
    data_server = models.CharField(max_length=50, verbose_name=u'数据服务器')
    chat_server = models.CharField(max_length=50, verbose_name=u'聊天服务器')
    web_server = models.CharField(max_length=50, verbose_name=u'web服务器')
    deploy_path = models.CharField(max_length=200, verbose_name=u'部署路径')
    db_server = models.CharField(max_length=50, verbose_name=u'数据库服务器')
    timestamp = models.DateTimeField(verbose_name=u'操作时间', auto_now=True)
    status = models.BooleanField(verbose_name=u'结果状态', default=False)
    context = models.TextField(verbose_name=u'结果详情', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('view deploy wizard', 'Can view deploy wizard'),
        )
