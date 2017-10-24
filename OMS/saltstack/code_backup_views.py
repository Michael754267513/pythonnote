# --*-- coding: utf-8 --*--

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404, get_object_or_404, HttpResponse
from models import Backup
from forms import BackupForm
from saltstack.scripts.salt_api import *
from saltstack.scripts.re_match_result import regex_match_error
from datetime import datetime


@login_required(login_url='/accounts/login/')
@permission_required('Salt.view_release', raise_exception=True)
def code_backup_list(request, template_name='saltstack/code_backup_list.html'):
    username = request.session['username']
    backup_list = Backup.objects.all()
    highlight11 = 'active'
    var7 = 'active'
    return render(request, template_name, locals())


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.view_backup', raise_exception=True)
def code_backup_process(request, template_name='saltstack/code_backup_form.html'):
    global status
    form = BackupForm(request.POST or None)
    if form.is_valid():
        zone_name = form.cleaned_data['zones'].name
        deploy_path = form.cleaned_data['deploy_path'].path_value
        # versions = form.cleaned_data['versions']
        project_name = form.cleaned_data['repository_name'].repo_tag
        backup_path = form.cleaned_data['backup_path'].path_value

        if form.cleaned_data['use_zone']:
            deploy_abs_path = os.path.join(deploy_path, (project_name + '_' + zone_name))
            code_backup_package = project_name + '_' + zone_name + '_' + datetime.now().strftime("%Y%m%d%H") + '.tar.gz'
        else:
            deploy_abs_path = os.path.join(deploy_path, project_name)
            code_backup_package = project_name + '_' + datetime.now().strftime("%Y%m%d%H") + '.tar.gz'

        shell_command = 'sh /data/agent_scripts/backup_code.sh %s %s %s' % (backup_path, deploy_abs_path,
                                                                            code_backup_package)

        code_backup_abs_path = os.path.join(backup_path, code_backup_package)

        data = {
            'expr_form': 'list',
            'client': form.cleaned_data['client'],
            'tgt': [item.host_name for item in form.cleaned_data['tgt']],
            'fun': 'cmd.run',
            'arg': shell_command,
        }

        print data
        salt = SaltApi()
        salt.get_token()
        header = salt.get_header()
        context = process(header, **data)
        print context

        for item in form.cleaned_data['tgt']:
            print yaml.load(context)['return'][0][item.host_name]
            if regex_match_error(context) is True:
                status = True
            else:
                status = False
        # Version.objects.filter(id=versions.id).update(vernier=u'2')
        new_form = form.save(commit=False)
        new_form.context = context
        new_form.deploy_path = deploy_abs_path
        new_form.backup_path = code_backup_abs_path
        new_form.fun = 'cmd.run'
        new_form.operate = request.session['username']
        new_form.status = status
        new_form.save()
        form.save()

        return redirect('code_backup_list')

    return render(request, template_name, {'highlight11': 'active',
                                           'username': request.session['username'],
                                           'form': form,
                                           'var7': 'active',
                                           })


@permission_required('Salt.view_release', raise_exception=True)
def code_backup_detail(request, pk, template_name='saltstack/code_backup_detail.html'):
    try:
        details = Backup.objects.get(pk=pk)
    except Backup.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight11': 'active'
                                           })


@login_required
@permission_required('Salt.delete_release', raise_exception=True)
def code_backup_record_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(Backup, pk=int(pk))
    # print histories.deploy_path
    # print histories.backup_path
    # print histories.tgt.all()
    shell_command = 'rm -rf %s' % histories.backup_path

    data = {
        'expr_form': 'list',
        'client': 'local',
        'tgt': histories.tgt.all(),
        'fun': 'cmd.run',
        'arg': shell_command,
    }
    print data

    salt = SaltApi()
    salt.get_token()
    header = salt.get_header()
    content = process(header, **data)
    print content
    histories.delete()
    return HttpResponse('delete success')
