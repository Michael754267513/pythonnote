# --*-- coding: utf-8 --*--

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404, HttpResponse, get_object_or_404
from forms import PackageInstallForm
from models import PackageInstall
from saltstack.scripts.re_match_result import regex_match_error
from saltstack.scripts.salt_api import *


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.add_packageinstall', raise_exception=True)
def yum_install_soft_record(request, template_name='saltstack/yum_install_soft_list.html'):
    packages = PackageInstall.objects.all()
    var7 = 'active'
    highlight10 = 'active'
    return render(request, template_name, locals())


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.add_packageinstall', raise_exception=True)
def yum_install_soft_process(request, template_name='saltstack/yum_install_soft_form.html'):
    form = PackageInstallForm(request.POST or None)
    server_list = []
    if form.is_valid():
        skip_verify = 'False'
        refresh = 'False'
        for item in form.cleaned_data['tgt']:
            server_list.append(item.host_name)
        data = {
            'expr_form': 'list',
            'client': 'local',
            'fun': form.cleaned_data['fun'],
            'tgt': server_list,
            'arg': [form.cleaned_data['yum_package_name'], refresh, skip_verify]
        }
        print data
        salt = SaltApi()
        salt.get_token()
        header = salt.get_header()
        context = process(header, **data)

        if regex_match_error(json.dumps(context)):
            status = True
        else:
            status = False

        new_form = form.save(commit=False)
        new_form.status = status
        new_form.context = context
        new_form.operate = request.session['username']
        new_form.save()
        form.save()

        return redirect('yum_install_soft_record')

    return render(request, template_name, {'form': form,
                                           'var7': 'active',
                                           'highlight10': 'active',
                                           'username': request.session['username'],
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.view_packageinstall', raise_exception=True)
def yum_install_soft_detail(request, pk, template_name='saltstack/yum_install_package_detail.html'):
    try:
        details = PackageInstall.objects.get(pk=pk)
    except PackageInstall.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight10': 'active'
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.delete_packageinstall', raise_exception=True)
def yum_install_record_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(PackageInstall, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')
