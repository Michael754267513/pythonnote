# --*-- coding: utf-8 --*--

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404, get_object_or_404, HttpResponse
from assets.models import Assets
from forms import UpdatesForm
from models import Updates
from saltstack.scripts.re_match_result import regex_match_error
from saltstack.scripts.salt_api import *
from s.models import
from oms_config.models import Zone, Path
from repository.models import Repository


# Create your views here.


@login_required
@permission_required('Salt.view_cron', raise_exception=True)
def all_zone_update_list(request, template_name='saltstack/all_zone_update_list.html'):
    username = request.session['username']
    updates = Updates.objects.all()
    highlight7 = 'active'
    var7 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('Salt.view_updates', raise_exception=True)
def all_zone_update_process(request, template_name='saltstack/all_zone_update_form.html'):
    s = .objects.all()
    zones = Zone.objects.all()
    path_object = Path.objects.filter(path_key__contains=u'部署')
    repo_object = Repository.objects.all()
    global status
    global commands
    global assets
    context = {}
    cmds = {}
    form = UpdatesForm(request.POST or None)
    if form.is_valid():
        # print form
        zone_list = form.cleaned_data['zones']
        repo_name = form.cleaned_data['repository_name']
        project_name = repo_name.repo_tag
        for zone in zone_list:
            host_list = []
            # print form.cleaned_data['use_zone']
            if form.cleaned_data['use_zone']:
                abs_path = os.path.join(form.cleaned_data['deploy_path'].path_value, (project_name + '_' + zone.name))
            else:
                abs_path = os.path.join(form.cleaned_data['deploy_path'].path_value, project_name)
            print abs_path
            commands = '%s %s' % (form.cleaned_data['commands'], abs_path)
            print commands
            cmds['%s' % zone] = commands

            assets = Assets.objects.filter(s=form.cleaned_data['s'], game_zone=zone)
            for item in assets:
                host_list.append(item.host_name)

            print host_list

            data = {
                'expr_form': 'list',
                'client': form.cleaned_data['client'],
                'fun': form.cleaned_data['fun'],
                'arg': commands,
                'tgt': host_list,
            }

            # print data

            if host_list:
                salt = SaltApi()
                salt.get_token()
                header = salt.get_header()
                context['%s' % zone] = process(header, **data)
            else:
                context['%s' % zone] = "not found servers"

        if regex_match_error(json.dumps(context)):
            status = True
        else:
            status = False

        new_form = form.save(commit=False)
        new_form.context = json.dumps(context, encoding='UTF-8', ensure_ascii=False)
        new_form.operate = request.session['username']
        new_form.status = status
        new_form.save()
        form.save()
        # updates = Updates(s=form.cleaned_data['s'],
        #                   operate=request.session['username'], client=form.cleaned_data['client'],
        #                   use_zone=form.cleaned_data['use_zone'], fun=form.cleaned_data['fun'],
        #                   commands=commands, deploy_path=form.cleaned_data['deploy_path'].path_value,
        #                   status=status, content=form.cleaned_data['content'], context=json.dumps(context),
        #                   repository_name_id=repo_name.id)
        # updates.save()
        # updates.tgt = assets
        # updates.zones = form.cleaned_data['zones']
        # updates.save()
        return redirect('all_zone_update_list')

    return render(request, template_name, {'form': form,
                                           'highlight7': 'active',
                                           'username': request.session['username'],
                                           'var7': 'active',
                                           's': s,
                                           'zones': zones,
                                           'path_object': path_object,
                                           'repo_object': repo_object,
                                           })


@login_required
@permission_required('Salt.view_updates', raise_exception=True)
def all_zone_update_detail(request, pk, template_name='saltstack/all_zone_update_detail.html'):
    try:
        details = Updates.objects.get(pk=pk)
    except Updates.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight7': 'active'
                                           })


@login_required
@permission_required('Salt.delete_updates', raise_exception=True)
def all_zone_update_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(Updates, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')
