# --*-- coding: utf-8 --*--

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404, get_object_or_404, HttpResponse
from models import RollBack
from forms import RollBackForm
from saltstack.scripts.salt_api import *
from saltstack.scripts.re_match_result import regex_match_error


@login_required(login_url='/accounts/login/')
@permission_required('Salt.view_release', raise_exception=True)
def code_rollback_list(request, template_name='saltstack/code_rollback_list.html'):
    username = request.session['username']
    rollback_list = RollBack.objects.all()
    highlight12 = 'active'
    var7 = 'active'
    return render(request, template_name, locals())


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.view_backup', raise_exception=True)
def code_rollback_process(request, template_name='saltstack/code_rollback_form.html'):
    global status
    form = RollBackForm(request.POST or None)
    if form.is_valid():
        project = form.cleaned_data['repository_name'].repo_tag
        zone_name = form.cleaned_data['zones'].name
        deploy_path = form.cleaned_data['deploy_path'].path_value
        backup_package = form.cleaned_data['backup_package'].backup_path
        print backup_package
        rollback_script = '/data/agent_scripts/rollback.sh'

        if form.cleaned_data['use_zone']:
            deploy_abs_path = os.path.join(deploy_path, (project + '_' + zone_name))
        else:
            deploy_abs_path = os.path.join(deploy_path, project)

        shell_command = "sh %s %s %s" % (rollback_script, backup_package, deploy_abs_path)
        data = {
            'expr_form': 'list',
            'client': form.cleaned_data['client'],
            'tgt': [server.host_name for server in form.cleaned_data['tgt']],
            'fun': 'cmd.run',
            'arg': shell_command,
        }

        print data
        salt = SaltApi()
        salt.get_token()
        header = salt.get_header()
        context = process(header, **data)
        # print context

        for item in form.cleaned_data['tgt']:
            if regex_match_error(yaml.load(context)['return'][0][item.host_name]):
                status = True
            else:
                status = False

        new_form = form.save(commit=False)
        new_form.context = context
        new_form.rollback_package = backup_package
        new_form.fun = 'cmd.run'
        new_form.operate = request.session['username']
        new_form.status = status
        new_form.save()
        form.save()

        return redirect('code_rollback_list')

    return render(request, template_name, {'highlight12': 'active',
                                           'username': request.session['username'],
                                           'form': form,
                                           'var7': 'active',
                                           })


@permission_required('Salt.view_release', raise_exception=True)
def code_rollback_detail(request, pk, template_name='saltstack/code_rollback_detail.html'):
    try:
        details = RollBack.objects.get(pk=pk)
    except RollBack.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight12': 'active'
                                           })


@login_required
@permission_required('Salt.delete_release', raise_exception=True)
def code_rollback_record_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(RollBack, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')
