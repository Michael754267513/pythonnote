# --*-- coding: utf-8 --*--

import json
import logging
# import sys
import threading
from django.contrib.auth.decorators import login_required
# from django.db.models import Q
from django.shortcuts import render, redirect
from OMS.settings import MASTER_IP
from assets.models import Assets
from forms import P2PForm
from repository.models import Repository
# from repository.models import Version
from saltstack.scripts.create_folder import makedir_p
from saltstack.scripts.execute_command import *
# from saltstack.scripts.get_newVersion_from_gitLog import get_version
from saltstack.scripts.re_match_result import regex_match_error
from saltstack.scripts.repo_process import *
from saltstack.scripts.salt_api import *

lock = threading.Lock()
lock_error = threading.Lock()
lock_result = threading.Lock()
num = 0
DESTINATION = []
SOURCE = []


def logging_out(message):
    logging.basicConfig(level=logging.INFO, filename="logs/all_client_scp.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info(message)


def add_error_list(server):
    lock_error.acquire()
    message = "error server: %s" % str(server)
    logging_out(message)
    lock_error.release()


def get_target_server():
    global num
    server = None
    lock.acquire()
    if num < len(DESTINATION):
        server = DESTINATION[num]
        num += 1
    lock.release()
    return server


def do_copy_control(source_server, source_path, compress_file, deploy_path, release_abs_path, md5sum):
    target_server = get_target_server()
    global return_result
    return_result = []
    while target_server:
        command = "/usr/bin/python /data/agent_scripts/scp_agent.py %s %s %s %s %s %s %s %s" % (
            source_server.networks.private_address,
            source_server.superuser,
            source_server.superuser_pass,
            source_path, deploy_path, release_abs_path, compress_file, md5sum
        )
        data = {
            'expr_form': 'list',
            'client': 'local',
            'fun': 'cmd.run',
            'tgt': target_server.host_name,
            'arg': command,
            }
        print data
        salt = SaltApi()
        salt.get_token()
        header = salt.get_header()
        context = process(header, **data)
        yaml_context = yaml.load(context)['return'][0]
        print yaml_context

        logging_out("source_server: %s  target_server: %s result: %s" % (source_server.host_name,
                                                                         target_server.host_name,
                                                                         yaml_context[target_server.host_name]))

        if yaml_context[target_server.host_name] or yaml_context[target_server.host_name] == 'already Latest!':
            result = {
                target_server.host_name: context
            }
            if return_result.append(result):
                thread = threading.Thread(target=do_copy_control, args=(target_server, source_path,
                                                                        compress_file, deploy_path,
                                                                        release_abs_path, md5sum))
                thread.start()
        else:
            add_error_list(target_server.host_name)
        target_server = get_target_server()


def get_destination_list(servers):
    for server in servers:
        DESTINATION.append(server)

    return DESTINATION


@login_required(login_url='/accounts/login/')
def p2p_scp_process(request, template_name='saltstack/code_release_form.html'):
    global status
    status = False
    form = P2PForm(request.POST or None)
    if form.is_valid():
        operate = request.session['username']
        # 项目名
        project = form.cleaned_data['repository_name'].repo_tag

        zones = form.cleaned_data['zones']
        # 归档路径
        archive_path = request.POST['archive_path']
        # 如果路径不存在，则创建
        if os.path.exists(archive_path):
            makedir_p(archive_path)

        # versions = form.cleaned_data['versions']
        get_deploy_path = form.cleaned_data['deploy_path'].path_value
        release_path = form.cleaned_data['release_path'].path_value

        # 部署路径 发布路径拼接
        if form.cleaned_data['use_zone']:
            deploy_path = os.path.join(get_deploy_path, (project + '_' + zones.name))
            release_abs_path = release_path + '_' + zones.name
        else:
            deploy_path = os.path.join(get_deploy_path, project)
            release_abs_path = release_path

        # 获取仓库地址
        repo_name = form.cleaned_data['repository_name']
        result = Repository.objects.filter(repo_name__contains=repo_name)[0]
        repository_url = get_repo_url(result)

        compress_file = os.path.join(archive_path, '%s.zip' % project)

        # 获取最新版并压缩
        git_checkout(archive_path, project, repository_url)
        archive_compress(archive_path, project, compress_file)

        # 获取md5码
        command = 'md5sum %s' % compress_file
        md5sum = get_md5sum(command)

        servers = form.cleaned_data['tgt']
        get_destination_list(servers)

        SOURCE.append(Assets.objects.filter(networks__private_address__icontains=MASTER_IP))
        source_server = SOURCE[0][0]

        do_copy_control(source_server, archive_path, compress_file, deploy_path, release_abs_path, md5sum)

        # print return_result

        for item in return_result:
            for key in item:
                if regex_match_error(item[key]) is True:
                    status = True
                else:
                    status = False
        # print status
        # store to mysql
        # Version.objects.filter(Q(vernier=u'1') | Q(vernier=u'2') | Q(vernier=u'3')).update(vernier=u'0')
        # if status:
        #     Version.objects.filter(id=versions.id).update(vernier=1)
        new_form = form.save(commit=False)
        new_form.fun = 'P2P_SCP'
        new_form.deploy_path = deploy_path
        new_form.release_path = release_abs_path
        new_form.operate = operate
        new_form.status = status
        new_form.context = json.dumps(return_result)
        new_form.save()
        form.save()
        return redirect('code_release_list')

    return render(request, template_name, {'form': form,
                                           'highlight2': 'active',
                                           'var7': 'active',
                                           })
