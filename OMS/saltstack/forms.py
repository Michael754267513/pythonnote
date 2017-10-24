# --*-- coding:utf8 --*--

from django import forms
from models import Release, Push, ServicesHandle, ExecuteCommand, Cron, Updates, SystemUserManager, Password
from models import PackageInstall, Backup, RollBack, SyncConfig, MergeServers
from oms_config.models import Path, Zone
from assets.models import Assets
from oms_config.models import Domain
from dbs_mysql.models import Databases


class ReleaseForm(forms.ModelForm):
    deploy_path = forms.ModelChoiceField(label=u'部署路径', queryset=Path.objects.filter(path_key__contains=u'部署路径'))
    release_path = forms.ModelChoiceField(label=u'发布路径', queryset=Path.objects.filter(path_key__contains=u'发布路径'))
    # versions = forms.ModelChoiceField(label=u'发布版本', queryset=Version.objects.filter(vernier=u'0'))
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    repo_archive_path = forms.CharField(max_length=200, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Release
        fields = '__all__'


class P2PForm(forms.ModelForm):
    deploy_path = forms.ModelChoiceField(label=u'部署路径', queryset=Path.objects.filter(path_key__contains=u'部署路径'))
    release_path = forms.ModelChoiceField(label=u'发布路径', queryset=Path.objects.filter(path_key__contains=u'发布路径'))
    # versions = forms.ModelChoiceField(label=u'发布版本', queryset=Version.objects.filter(vernier=u'0'))
    archive_path = forms.CharField(max_length=200, label=u'本地归档路径', initial=u'/srv/salt/code/project/')
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    fun = forms.CharField(label=u'执行模块', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Release
        fields = '__all__'


class BackupForm(forms.ModelForm):
    backup_path = forms.ModelChoiceField(label=u'备份路径', queryset=Path.objects.filter(path_key__contains=u'备份路径'))
    deploy_path = forms.ModelChoiceField(label=u'部署路径', queryset=Path.objects.filter(path_key__contains=u'部署路径'))
    # versions = forms.ModelChoiceField(label=u'发布版本', queryset=Version.objects.filter(vernier=u'1'))
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    fun = forms.CharField(label=u'执行模块', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Backup
        fields = '__all__'


class RollBackForm(forms.ModelForm):
    deploy_path = forms.ModelChoiceField(label=u'部署路径', queryset=Path.objects.filter(path_key__contains=u'部署路径'))
    release_path = forms.ModelChoiceField(label=u'发布路径', queryset=Path.objects.filter(path_key__contains=u'发布路径'))
    backup_package = forms.ModelChoiceField(label=u'备份包路径', queryset=Backup.objects.all())
    # versions = forms.ModelChoiceField(label=u'发布版本', queryset=Version.objects.filter(vernier=u'2'))
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    rollback_package = forms.CharField(max_length=200, label=u'回档包', widget=forms.HiddenInput(), required=False)
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    fun = forms.CharField(label=u'执行模块', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = RollBack
        fields = '__all__'


class PushForm(forms.ModelForm):
    SERVICE_CHOICE = (
        (u'1', u'nginx'),
        (u'2', u'tomcat'),
        (u'3', u'redis'),
        (u'4', u'php-fpm'),
    )

    service_name = forms.ChoiceField(label=u'服务名', choices=SERVICE_CHOICE, widget=forms.RadioSelect )
    fun = forms.CharField(label=u'模块', max_length=20, widget=forms.HiddenInput(), required=False)
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Push
        fields = '__all__'


class Unix2DosForm(forms.Form):
    file = forms.CharField(label=u'文件名', max_length=200, error_messages={'required': u'必填输入绝对路径'})
    tgt = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                         queryset=Assets.objects.filter(is_online=True),
                                         label=u'选择服务器')
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super(Unix2DosForm, self).clean()
        return cleaned_data


class ServicesHandleForm(forms.ModelForm):
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    client = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), initial=u'local')
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ServicesHandle
        fields = '__all__'


class ExecuteCommandForm(forms.ModelForm):
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    client = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), initial=u'local')
    fun = forms.CharField(max_length=100, label=u'操作用户', widget=forms.HiddenInput(), initial=u'local')
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ExecuteCommand
        fields = '__all__'


class CronForm(forms.ModelForm):
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Cron
        fields = '__all__'


class UpdatesForm(forms.ModelForm):
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    zones = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Zone.objects.all(),
                                           label=u'选择分区')
    deploy_path = forms.ModelChoiceField(label=u'部署路径', queryset=Path.objects.all())
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    client = forms.CharField(label=u'发送指令主机', widget=forms.HiddenInput(), required=False)
    fun = forms.CharField(label=u'执行模块', widget=forms.HiddenInput(), required=False)
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Updates
        fields = '__all__'


class SystemUserAddForm(forms.ModelForm):
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = SystemUserManager
        fields = '__all__'


class SystemUserDelForm(forms.ModelForm):
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    fun = forms.CharField(label=u'执行模块', initial='user.delete')
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = SystemUserManager
        fields = '__all__'


class PasswordFrom(forms.ModelForm):
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Password
        fields = '__all__'


class PackageInstallForm(forms.ModelForm):
    tgt = forms.ModelMultipleChoiceField(label=u'目标主机', queryset=Assets.objects.filter(is_online=True))
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PackageInstall
        fields = '__all__'


class SyncConfigForm(forms.ModelForm):
    salt_url = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    dest_path = forms.ModelChoiceField(label=u'部署路径', queryset=Path.objects.filter(path_key__contains=u'部署路径'))
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = SyncConfig
        fields = '__all__'


class MergeServersForm(forms.ModelForm):
    merge_zones = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Zone.objects.all(),
                                                 label=u'选择分区')
    operate = forms.CharField(max_length=20, label=u'操作用户', widget=forms.HiddenInput(), required=False)
    status = forms.BooleanField(label=u'是否成功', widget=forms.HiddenInput(), required=False)
    context = forms.CharField(max_length=2000, label=u'执行结果', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = MergeServers
        fields = '__all__'


class DeployGameWizardForm(forms.Form):
    zones = forms.ModelChoiceField(label=u'选择分区', queryset=Zone.objects.all())
    domain = forms.ModelChoiceField(label=u'选择域名', queryset=Domain.objects.all())
    server_id = forms.CharField(label=u'服务ID', max_length=20)
    tx_id = forms.CharField(label=u'腾讯ID', max_length=20)
    war_server = forms.ModelChoiceField(label=u'war服务器', queryset=Assets.objects.all())
    chat_server = forms.ModelChoiceField(label=u'聊天聊务器', queryset=Assets.objects.all())
    db_server = forms.ModelChoiceField(label=u'选择数据库服务器', queryset=Databases.objects.all())

