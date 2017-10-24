# --*-- coding: utf-8 --*--

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
# from assets.models import Assets
# from s.models import
from forms import SyncConfigForm
from models import SyncConfig
from oms_config.models import Information
# from oms_config.models import Zone
# from repository.models import Repository
# from repository.models import Version
from saltstack.scripts.salt_api import *
from saltstack.scripts.re_match_result import regex_match_error
# from django.db.models import Q


@login_required
@permission_required('Salt.view_syncconfig', raise_exception=True)
def sync_config_list(request, template_name='saltstack/sync_config_list.html'):
    username = request.session['username']
    records = SyncConfig.objects.all()
    highlight14 = 'active'
    var7 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('Salt.add_syncconfig', raise_exception=True)
def sync_config_process(request, template_name='saltstack/sync_config_form.html'):
    form = SyncConfigForm(request.POST or None)
    if form.is_valid():
        project_name = form.cleaned_data['repository'].repo_tag
        zone = form.cleaned_data['zones'].name
        salt_url = os.path.join('salt://app_config', zone)
        print salt_url
        dest_path = form.cleaned_data['dest_path'].path_value
        if form.cleaned_data['use_zone']:
            salt_abs_url = os.path.join(salt_url, (project_name + '_' + zone))
        else:
            salt_abs_url = os.path.join(salt_url, project_name)

        data = {
            'expr_form': 'list',
            'client': 'local',
            'fun': 'cp.get_dir',
            'tgt': [item.host_name for item in form.cleaned_data['tgt'].all()],
            'arg': [salt_abs_url, dest_path],
        }
        print data

        salt = SaltApi()
        salt.get_token()
        header = salt.get_header()
        context = process(header, **data)
        print context

        if project_name == 'pxqb_login':
            info = Information.objects.filter(zones=form.cleaned_data['zones'], key__contains="SERVER_ID")
            if info:
                for item in info:
                    server_id = item.value
                    filename = os.path.join(dest_path, project_name + '_' + zone, 'server.php')
                    command = "sh /data/agent_scripts/enable_entrance.sh %s %s" % (server_id, filename)

                    data = {
                        'expr_form': 'list',
                        'client': 'local',
                        'fun': 'cmd.run',
                        'tgt': [item.host_name for item in form.cleaned_data['tgt'].all()],
                        'arg': command,
                    }

                    print data

                    salt = SaltApi()
                    salt.get_token()
                    header = salt.get_header()
                    result = process(header, **data)
                    print result

        if regex_match_error(context):
            status = True
        else:
            status = False
        new_form = form.save(commit=False)
        new_form.operate = request.session['username']
        new_form.dest_path = dest_path
        new_form.salt_url = salt_abs_url
        new_form.status = status
        new_form.context = context
        new_form.save()
        form.save()

        return redirect('sync_config_list')

    return render(request, template_name, {'highlight14': 'active',
                                           'username': request.session['username'],
                                           'form': form,
                                           'var7': 'active',
                                           })


@login_required
@permission_required('Salt.delete_syncconfig', raise_exception=True)
def sync_config_record_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(SyncConfig, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('saltstack.view_syncconfig', raise_exception=True)
def sync_config_detail(request, pk, template_name='saltstack/sync_config_detail.html'):
    try:
        details = SyncConfig.objects.get(pk=pk)
    except SyncConfig.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight14': 'active'
                                           })
