# --*-- coding: utf-8 --*--

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from assets.models import Assets
from s.models import
from forms import MergeServersForm
from models import MergeServers
from scripts.create_folder import makedir_p
from scripts.execute_command import running_command
from oms_config.models import Zone
from repository.models import Repository
from saltstack.scripts.salt_api import *
from scripts.merge_pxqb_base_conf import merge_all_server, do_copy_new_file
from oms_config.generate_file import execute_replace
from saltstack.scripts.re_match_result import regex_match_error
import json


@login_required
@permission_required('saltstack.view_mergeservers', raise_exception=True)
def merge_server_list(request, template_name='saltstack/merge_server_list.html'):
    username = request.session['username']
    records = MergeServers.objects.all()
    highlight13 = 'active'
    var7 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('saltstack.add_mergeservers', raise_exception=True)
def merge_server_process(request, template_name='saltstack/merge_server_form.html'):
    s = .objects.all()
    zones = Zone.objects.all()
    # repo_object = Repository.objects.filter(repo_tag=u'war_data')
    repo_object = Repository.objects.all()
    assets = Assets.objects.all()
    war_object = Assets.objects.filter(tag__name='War')
    chat_object = Assets.objects.filter(tag__name='Chat')
    web_object = Assets.objects.filter(tag__name='Web')

    zone_list = []
    form = MergeServersForm(request.POST or None)
    if form.is_valid():
        information = {}
        context = {}
        war_server_id = form.cleaned_data['data_server']
        chat_server_id = form.cleaned_data['chat_server']
        war_servers = Assets.objects.filter(id=war_server_id)
        for item in war_servers:
            information['{{WAR_DATA_HOST}}'] = item.alias_name
            information['{{WAR_DATA_ADDR}}'] = item.networks.private_address
            information['{{REDIS_ADDR}}'] = item.networks.private_address

        chat_servers = Assets.objects.filter(id=chat_server_id)
        for item in chat_servers:
            information['{{CHAT_PUBLIC_ADDR}}'] = item.networks.public_address
            information['{{CHAT_PRIVATE_ADDR}}'] = item.networks.private_address
            information['{{CHAT_HOST}}'] = item.alias_name

        project_list = ['war_data', 'pxqb_base', 'pxqb_login']

        merge_path = form.cleaned_data['merge_path']
        # print merge_path

        if not os.path.exists(merge_path):
            makedir_p(merge_path)

        merge_zones = form.cleaned_data['merge_zones']

        for zone in merge_zones:
            zone_list.append(zone.name)

        zone_shell_array = ' '.join(zone_list)
        # print zone_shell_array
        merge_name = '_'.join(zone_list)
        # print merge_name

        deploy_path = '/data/deploy'

        source_path = '/srv/salt/app_config'

        # 合并、复制、生成新配置
        for project_name in project_list:
            if project_name == 'war_data':
                script = "sh /data/deploy/OMS/saltstack/scripts/shell/merge_config_file.sh '%s' '%s' '%s' '%s' '%s'" \
                          % (source_path, merge_path, zone_shell_array, merge_name, project_name)
                # print script
                running_command(script)

            if project_name == 'pxqb_base':
                project_abs_path = os.path.join(merge_path, merge_name, project_name, 'config')
                if not os.path.exists(project_abs_path):
                    makedir_p(project_abs_path)

                # 合并conf.allserver.php文件
                file_list = []
                for zone in zone_list:
                    file_list.append('%s/%s/%s/config/conf.allserver.php' % (source_path, zone, project_name))
                # print file_list
                one_file = file_list[0]
                do_copy_new_file(one_file, merge_name)
                file_list.pop(0)
                # print file_list
                merge_all_server(file_list, merge_name)

                # 生成新dataserver.php文件
                dataserver_file = '/data/deploy/OMS/media/Upload/conf.dataserver.php'
                merge_target_file = '/srv/salt/merge_config/%s/pxqb_base/config/conf.dataserver.php' % merge_name
                execute_replace(information, dataserver_file, merge_target_file)

            if project_name == 'pxqb_login':
                for zone in zone_list:
                    full_project_name = project_name + '_' + zone
                    copy_target_path = os.path.join(merge_path, merge_name)
                    if not os.path.exists(copy_target_path):
                        makedir_p(copy_target_path)
                    script = "sh /data/deploy/OMS/saltstack/scripts/shell/copy_pxqb_login_config.sh %s %s %s" \
                             % (full_project_name, copy_target_path, zone)
                    # print script
                    running_command(script)

        # 同步配置
        project_tmp = project_list
        for project_name in project_list:
            if project_name == 'pxqb_login':
                for zone in zone_list:
                    project_tmp.append(project_name + '_' + zone)

        project_tmp.remove('pxqb_login')

        for project_name in project_tmp:
            salt_abs_url = 'salt://merge_config/%s/%s' % (merge_name, project_name)
            data = {
                'expr_form': 'list',
                'client': 'local',
                'fun': 'cp.get_dir',
                'tgt': [item.host_name for item in form.cleaned_data['tgt'].all()],
                'arg': [salt_abs_url, deploy_path],
            }
            # print data
            salt = SaltApi()
            salt.get_token()
            header = salt.get_header()
            context['%s' % project_name] = process(header, **data)
            print context['%s' % project_name]

        print context

        if regex_match_error(json.dumps(context)):
            status = True
        else:
            status = False
        new_form = form.save(commit=False)
        new_form.operate = request.session['username']
        new_form.status = status
        new_form.chat_server = information['{{CHAT_HOST}}']
        new_form.data_server = information['{{WAR_DATA_HOST}}']
        new_form.context = json.dumps(context)
        new_form.save()
        form.save()

        return redirect('merge_server_list')

    return render(request, template_name, {'highlight13': 'active',
                                           'username': request.session['username'],
                                           'form': form,
                                           'var7': 'active',
                                           'repo_object': repo_object,
                                           'assets': assets,
                                           'zones': zones,
                                           's': s,
                                           'war_object': war_object,
                                           'web_object': web_object,
                                           'chat_object': chat_object,
                                           })


@login_required
@permission_required('saltstack.delete_mergeservers', raise_exception=True)
def merge_server_record_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(MergeServers, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('saltstack.view_mergeservers', raise_exception=True)
def merge_server_detail(request, pk, template_name='saltstack/merge_server_detail.html'):
    try:
        details = MergeServers.objects.get(pk=pk)
    except MergeServers.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight13': 'active'
                                           })
