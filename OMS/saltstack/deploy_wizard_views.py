# --*-- coding: utf-8 --*--

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, HttpResponse, Http404, get_object_or_404
from assets.models import Assets, Services
from models import RELEASE_FUN_CHOICES, DeployWizard
from saltstack.scripts.salt_api import *
from s.models import
from dbs_mysql.models import Databases
from oms_config.models import Domain, Zone, Path, Upload, Information
from oms_config.generate_file import *
from saltstack.scripts.create_folder import makedir_p
from scripts.execute_command import running_command
from scripts.re_match_result import regex_match_error
from OMS.settings import web_login_git_url, war_data_git_url, web_base_git_url
import copy
import json

# Create your views here.


@login_required(login_url='/accounts/login/')
def deploy_game_wizard_list(request, template_name='saltstack/deploy_game_wizard_list.html'):
    username = request.session['username']
    records = DeployWizard.objects.all()
    highlight15 = 'active'
    var7 = 'active'
    return render(request, template_name, locals())


@login_required(login_url='/accounts/login/')
def deploy_game_wizard(request, template_name='saltstack/deploy_game_wizard.html'):
    s = .objects.all()
    war_servers = Assets.objects.filter(tag__name='War')
    db_servers = Databases.objects.all()
    domains = Domain.objects.all()
    zones = Zone.objects.all()
    web_servers = Assets.objects.filter(tag__name='Web')
    chat_servers = Assets.objects.filter(tag__name='Chat')
    path_object = Path.objects.filter(path_key__contains=u'部署路径')
    services = Services.objects.all()

    if request.method == 'POST':
        start_date = '2018-06-01'
        start_time = '09-00-00'
        sql_file = 'war.sql'

        upload_files = Upload.objects.all()
        config_files = []

        for item in upload_files:
            config_files.append(item.doc_file.name)

        information = {}
        replacements = {}
        config_path = {}
        context = {}

        zone_object = Zone.objects.filter(id=request.POST.get('zones'))
        for item in zone_object:
            information['zone'] = item.name
            information['ZONE_NAME'] = item.content

        domain_object = Domain.objects.filter(id=request.POST.get('domain'))
        for item in domain_object:
            information['domain'] = item.name

        war_server_object = Assets.objects.filter(id=request.POST.get('war_servers'))
        for item in war_server_object:
            information['WAR_DATA_ADDR'] = item.networks.private_address
            information['REDIS_ADDR'] = item.networks.private_address
            information['WAR_DATA_HOST'] = item.host_name
            information['WAR_TAGS'] = [tag.name for tag in item.tag.all()]

        chat_server_object = Assets.objects.filter(id=request.POST.get('chat_servers'))
        for item in chat_server_object:
            information['CHAT_HOST_NAME'] = item.alias_name
            information['CHAT_PRIVATE_ADDR'] = item.networks.private_address
            information['CHAT_PUBLIC_ADDR'] = item.networks.public_address
            information['CHAT_TAGS'] = [tag.name for tag in item.tag.all()]

        db_server_object = Databases.objects.filter(id=request.POST.get('db_server'))
        for item in db_server_object:
            information['MYSQL_ADDR'] = item.ip_address
            information['MYSQL_USER'] = item.schema_user
            information['MYSQL_PASS'] = item.schema_pass

        information['SERVER_ID'] = request.POST.get('server_id')

        information['TX_SID'] = request.POST.get('tx_id')

        web_server_object = Assets.objects.filter(id=request.POST.get('web_servers'))
        for item in web_server_object:
            information['WEB_SERVER_HOST'] = item.host_name
            information['WEB_TAGS'] = [tag.name for tag in item.tag.all()]

        deploy_path_object = Path.objects.filter(id=request.POST.get('deploy_path'))

        for item in deploy_path_object:
            information['deploy_path'] = item.path_value

        fun_value = dict(RELEASE_FUN_CHOICES).get(request.POST.get('fun'))

        # 存入键值到Information库
        store_dict = copy.copy(information)
        remove_list = ['zone', 'domain', 'deploy_path', 'WEB_SERVER_HOST',
                       'WAR_DATA_HOST', 'MYSQL_USER', 'CHAT_HOST_NAME', 'WAR_TAGS',
                       'CHAT_TAGS', 'WEB_TAGS', 'ZONE_NAME']
        for key in remove_list:
            store_dict.pop(key)

        info_queryset = Information.objects.filter(zones_id=request.POST.get('zones'))
        if not info_queryset:
            for key in store_dict:
                info = Information(zones_id=request.POST.get('zones'), key=key, value=information[key])
                info.save()
                print "insert success!"
        else:
            for item in info_queryset:
                for key in store_dict:
                    queryset = Information.objects.filter(zones_id=request.POST.get('zones'), id=item.id, key=key)
                    if queryset:
                        if queryset.update(value=information[key]):
                            print "update success!"

        # 定义配置生成目录
        config_path['war_config_path'] = '/srv/salt/app_config/%s/war_data/war_data/WEB-INF' % information['zone']
        config_path['web_base_path'] = '/srv/salt/app_config/%s/pxqb_base/config' % information['zone']
        config_path['web_login_path'] = '/srv/salt/app_config/%s/pxqb_login_%s' % (information['zone'],
                                                                                   information['zone'])
        config_path['nginx_config_path'] = '/srv/salt/service_config/%s' % information['zone']

        for key in config_path:
            if not os.path.exists(config_path[key]):
                makedir_p(config_path[key])

        for key in information:
            replacements['{{%s}}' % key] = information[key]

        # 导入sql
        context['import_sql'] = do_import_sql(start_date, start_time, sql_file, **information)

        # 记录进数据库
        dbs = Databases.objects.filter(ip_address=information['MYSQL_ADDR'])
        for item in dbs:
            item.zones.add(request.POST.get('zones'))

        if not request.POST.get('merge'):
            # 调用配置生成函数
            do_replace_config_file(config_path, config_files, replacements)

            # 部署war_data代码
            war_data_deploy_path = os.path.join(information['deploy_path'], 'war_data')
            # 备份清理旧的代码
            for hostname in [information['WAR_DATA_HOST'], information['WEB_SERVER_HOST']]:
                context['%s_do_backup_and_clear' % hostname] = do_backup_clear_old_package(hostname)

            if 'War' in information['WAR_TAGS']:
                context['deploy_war_data'] = do_deploy_project_to_remote_machine(
                        information['WAR_DATA_HOST'], fun_value, [war_data_deploy_path, war_data_git_url]
                )
                # 创建软链
                release_path = '/data/wardata'
                shell = 'if test -L %s;then echo "already release!";' \
                        'else ln -s %s %s && echo "make symlink success!";fi' \
                        % (release_path, war_data_deploy_path, release_path)

                context['war_data_make_symlink'] = do_deploy_project_to_remote_machine(
                        information['WAR_DATA_HOST'], 'cmd.run', shell)

            # 部署base和login
            if 'Web' in information['WEB_TAGS']:
                object_list = ['pxqb_base', 'pxqb_login_%s' % information['zone']]
                for project in object_list:
                    print project
                    web_deploy_path = os.path.join(information['deploy_path'], project)
                    web_release_path = os.path.join('/data/wwwroot', project)
                    if project == 'pxqb_base':
                        git_url = web_base_git_url
                    else:
                        git_url = web_login_git_url

                    context['deploy_%s' % project] = do_deploy_project_to_remote_machine(
                            information['WEB_SERVER_HOST'], fun_value, [web_deploy_path, git_url]
                    )
                    # make symlink
                    shell = 'if test -L %s;then echo "already make symlink!";' \
                            'else mkdir -p /data/wwwroot && ln -s %s %s && echo "make symlink success!";fi' % \
                            (web_release_path, web_deploy_path, web_release_path)

                    context['%s_make_symlink' % project] = do_deploy_project_to_remote_machine(
                            information['WEB_SERVER_HOST'], 'cmd.run', shell
                    )

                    # 同步base和login配置文件
                    object_config_salt_url = "salt://app_config/%s/%s" % (information['zone'], project)
                    print object_config_salt_url
                    context['%s_config_sync' % project] = do_deploy_project_to_remote_machine(
                            information['WEB_SERVER_HOST'], 'cp.get_dir', [object_config_salt_url,
                                                                           information['deploy_path']])

                # 同步web服务配置
                context['%s_sync_web_conf' % information['zone']] = do_sync_web_conf(information)

        else:
            # 生成配置文件并进行文件对比合并
            zone2_object = Zone.objects.filter(id=request.POST.get('previous_zone'))
            for item in zone2_object:
                information['previous_zone'] = item.name

            do_replace_config_file(config_path, config_files, replacements)

            # 配置文件比对，合并
            source_root_path = '/srv/salt/app_config'                # 原配置根目录
            shared_root_path = '/srv/salt/shared_war_server'               # 共用war配置根目录
            merge_name = '%s_%s' % (information['previous_zone'], information['zone'])            # 合并目录名
            zone_shell_array = '%s %s' % (information['previous_zone'], information['zone'])      # 游戏分区数组 shell用

            project_name = 'war_data'
            command = "sh /data/deploy/OMS/saltstack/scripts/shell/merge_config_file.sh '%s' '%s' '%s' '%s' '%s'" \
                      % (source_root_path, shared_root_path, zone_shell_array, merge_name, project_name)
            # 执行合并脚本
            running_command(command)

            # 第一次已经同步war_data代码，所以这里只同步war_data配置文件
            war_config_salt_url = "salt://shared_war_server/%s_%s/war_data" % \
                                  (information['previous_zone'], information['zone'])

            context['war_data_config_sync'] = do_deploy_project_to_remote_machine(
                    information['WAR_DATA_HOST'], 'cp.get_dir', [war_config_salt_url, information['deploy_path']]
            )

            # 备份清理旧的包
            context['%s_do_backup_and_clear' % information['WEB_SERVER_HOST']] = \
                do_backup_clear_old_package(information['WEB_SERVER_HOST'])

            object_list = ['pxqb_base', 'pxqb_login_%s' % information['zone']]
            for project in object_list:
                web_deploy_path = os.path.join(information['deploy_path'], project)
                web_release_path = os.path.join('/data/wwwroot', project)
                if project == 'pxqb_base':
                    git_url = web_base_git_url
                else:
                    git_url = web_login_git_url

                context['deploy_%s' % project] = do_deploy_project_to_remote_machine(
                        information['WEB_SERVER_HOST'], fun_value, [web_deploy_path, git_url]
                )
                # make symlink
                shell = 'if test -L %s;then echo "already make symlink!";' \
                        'else mkdir -p /data/wwwroot && ln -s %s %s && echo "make symlink success!";fi' % \
                        (web_release_path, web_deploy_path, web_release_path)

                context['%s_make_symlink' % project] = do_deploy_project_to_remote_machine(
                        information['WEB_SERVER_HOST'], 'cmd.run', shell
                )

                # 同步配置
                object_config_salt_url = "salt://app_config/%s/%s" % (information['zone'], project)

                context['%s_config_sync' % project] = do_deploy_project_to_remote_machine(
                    information['WEB_SERVER_HOST'], 'cp.get_dir', [object_config_salt_url, information['deploy_path']]
                )

            # 同步web服务配置
            context['%s_sync_nginx_conf' % information['zone']] = do_sync_web_conf(information)

        print json.dumps(context)

        # 重启进服务

        if regex_match_error(json.dumps(context)):
            status = True
        else:
            status = False
        deploy_wizard_object = DeployWizard(s_id=u'1',
                                            zones_id=int(request.POST.get('zones')),
                                            operate=request.session['username'],
                                            data_server=information['WAR_DATA_HOST'],
                                            chat_server=information['CHAT_HOST_NAME'],
                                            web_server=information['WEB_SERVER_HOST'],
                                            db_server=information['MYSQL_ADDR'],
                                            deploy_path=information['deploy_path'],
                                            status=status, context=json.dumps(context, sort_keys=True))
        deploy_wizard_object.save()

        return redirect('deploy_game_wizard_list')

    return render(request, template_name, {'s': s,
                                           'username': request.session['username'],
                                           'var7': "active",
                                           'highlight15': "active",
                                           'war_servers': war_servers,
                                           'db_servers': db_servers,
                                           'web_servers': web_servers,
                                           'chat_servers': chat_servers,
                                           'domains': domains,
                                           'zones': zones,
                                           'path_object': path_object,
                                           'services': services
                                           })


def do_salt_operate(**data):
    salt = SaltApi()
    salt.get_token()
    header = salt.get_header()
    context = process(header, **data)
    return context


def do_replace_config_file(config_path, config_files, replacements):
    for config_file in config_files:
        file_name = os.path.basename(config_file)
        if file_name == 'server.php':
            generate_file = os.path.join(config_path['web_login_path'], file_name)
        elif file_name == 'conf.allserver.php' or file_name == 'conf.dataserver.php':
            generate_file = os.path.join(config_path['web_base_path'], file_name)
        elif file_name == 'vhost.conf':
            generate_file = os.path.join(config_path['nginx_config_path'], file_name)
        else:
            generate_file = os.path.join(config_path['war_config_path'], file_name)

        print generate_file

        execute_replace(replacements, config_file, generate_file)


def do_import_sql(start_date, start_time, sql_file, **data):
    scripts = "sh /data/agent_scripts/replace_sql_string.sh %s %s %s %s %s %s %s" \
              % (sql_file, data['SERVER_ID'], data['ZONE_NAME'], start_date, start_time,
                 data['MYSQL_ADDR'], data['MYSQL_PASS'])
    new_data = {
        'expr_form': 'list',
        'client': 'local',
        'fun': 'cmd.run',
        'tgt': data['WAR_DATA_HOST'],
        'arg': scripts,
    }

    return do_salt_operate(**new_data)


def do_sync_web_conf(information):
    template = 'jinja'
    env = 'base'
    makedirs = False
    file_name = 'vhost.conf'
    nginx_file_system_url = "salt://service_config/%s/%s" % (information['zone'], file_name)
    target_abs_path = '/usr/local/lnmp/nginx/conf/vhosts/%s_vhost.conf' % information['zone']
    data = {
        'expr_form': 'list',
        'client': 'local',
        'fun': 'cp.get_template',
        'tgt': information['WEB_SERVER_HOST'],
        'arg': [nginx_file_system_url, target_abs_path, template, env, makedirs],
    }

    return do_salt_operate(**data)


def do_backup_clear_old_package(hostname):
    scripts = "sh /data/agent_scripts/backup_and_clear_old_version.sh"
    data = {
        'expr_form': 'list',
        'client': 'local',
        'fun': 'cmd.run',
        'tgt': hostname,
        'arg': scripts,
    }

    return do_salt_operate(**data)


def do_deploy_project_to_remote_machine(hostname, fun, args):
    data = {
        'expr_form': 'list',
        'client': 'local',
        'tgt': hostname,
        'fun': fun,
        'arg': args,
    }

    return do_salt_operate(**data)


@login_required
@permission_required('Salt.view_release', raise_exception=True)
def deploy_game_wizard_detail(request, pk, template_name='saltstack/deploy_game_wizard_detail.html'):
    try:
        details = DeployWizard.objects.get(pk=pk)
    except DeployWizard.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight15': 'active'
                                           })


@login_required
@permission_required('Salt.delete_release', raise_exception=True)
def deploy_game_wizard_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(DeployWizard, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')
