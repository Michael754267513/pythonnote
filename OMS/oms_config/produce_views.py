# --*-- coding: utf-8 --*--

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from models import Produce, Information
from forms import ProduceForm
from saltstack.scripts.create_folder import makedir_p
from s.models import
from models import Zone, Upload, Path
from repository.models import Repository
# from dbs_mysql.models import MySQL, DBAccounts
from generate_file import *
import os
# import re
# from OMS.settings import SALT_FILES_ROOT
# from assets.models import Assets
# from mkdirs import create_folder


@login_required
@permission_required('oms_config.view_produce', raise_exception=True)
def produce_list(request, template_name='oms_config/produce_list.html'):
    username = request.session['username']
    produces = Produce.objects.all()
    var4 = 'active'
    highlight5 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('Games.add_produce', raise_exception=True)
def produce_add(request, template_name='oms_config/produce_add.html'):
    s = .objects.all()
    zones = Zone.objects.all()
    config_files = Upload.objects.all()
    generate_object = Path.objects.filter(path_key__contains=u'配置生成目录')
    repo_object = Repository.objects.all()
    generate_file_list = []
    replacements = {}
    form = ProduceForm(request.POST or None)
    username = request.session['username']
    if form.is_valid():
        project_name = form.cleaned_data['project_name'].repo_tag
        zone_list = form.cleaned_data['zones']
        config_file = str(form.cleaned_data['config_file'].doc_file)
        for item in zone_list:
            # print item.name
            generate_path = form.cleaned_data['generate_path'].path_value
            if project_name == 'war_data':
                generate_abs_path = os.path.join(generate_path, item.name, project_name, project_name, 'WEB-INF')
            elif project_name == 'pxqb_login':
                generate_abs_path = os.path.join(generate_path, item.name, project_name + '_' + item.name)
            else:
                generate_abs_path = os.path.join(generate_path, item.name, project_name, 'config')
            basename = os.path.basename(config_file)
            if not os.path.exists(generate_abs_path):
                makedir_p(generate_abs_path)
            generate_file = os.path.join(generate_abs_path, basename)
            generate_file_list.append(generate_file)
            # replacements['{{ZONES}}'] = zone_name
            info = Information.objects.filter(zones=item)
            for x in info:
                replacements['{{%s}}' % x.key] = x.value
        # print replacements
        # print generate_file_list
        for abs_file in generate_file_list:
            execute_replace(replacements, config_file, abs_file)

        new_form = form.save(commit=False)
        new_form.generate_path = generate_file_list
        new_form.save()
        form.save()

        return redirect('produce_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var4': 'active',
                                           'highlight5': 'active',
                                           's': s,
                                           'zones': zones,
                                           'config_files': config_files,
                                           'generate_object': generate_object,
                                           'repo_object': repo_object,
                                           })


@login_required
@permission_required('Games.change_produce', raise_exception=True)
def produce_edit(request, pk, template_name='oms_config/produce_add.html'):
    username = request.session['username']
    produces = get_object_or_404(Produce, pk=pk)
    form = ProduceForm(request.POST or None, instance=produces)
    if form.is_valid():
        form.save()
        return redirect('produce_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var4': 'active',
                                           'highlight5': 'active',
                                           })


@login_required
@permission_required('Games.delete_produce', raise_exception=True)
def produce_del(request):
    pk = request.GET['id']
    produces = get_object_or_404(Produce, pk=int(pk))
    produces.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('GameConf.view_produce', raise_exception=True)
def produce_detail(request, pk, template_name='oms_config/produce_detail.html'):
    try:
        produces = Produce.objects.get(pk=pk)
        # information = Information.objects.filter(zones=[x for x in produces.zones.all()])
    except Produce.DoesNotExist:
        raise Http404
    return render(request, template_name, {'produces': produces,
                                           # 'information': information,
                                           'var4': 'active',
                                           'highlight5': 'active',
                                           'username': request.session['username'],
                                           })
