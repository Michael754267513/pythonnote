# --*-- coding: utf-8 --*--

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404, get_object_or_404, HttpResponse

from assets.models import SysUser
from forms import SystemUserAddForm, SystemUserDelForm
from models import SystemUserManager
from saltstack.scripts.re_match_result import regex_match_error
from saltstack.scripts.salt_api import *


# Create your views here.


@login_required(login_url='/accounts/login')
@permission_required('saltstack.view_systemusermanager', raise_exception=True)
def system_user_list(request, template_name='saltstack/system_user_list.html'):
    username = request.session['username']
    operates = SystemUserManager.objects.all()
    highlight8 = 'active'
    var7 = 'active'

    return render(request, template_name, locals())


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.add_systemusermanager', raise_exception=True)
def system_user_add(request, template_name='saltstack/system_user_form.html'):
    form = SystemUserAddForm(request.POST or None)
    hosts = []
    if form.is_valid():
        for item in form.cleaned_data['tgt']:
            print item.host_name
            hosts.append(item.host_name)

        data = {
            'expr_form': 'list',
            'client': form.cleaned_data['client'],
            'tgt': hosts,
            'fun': form.cleaned_data['fun'],
            'arg': [form.cleaned_data['user'], 'home=%s' %
                    os.path.join(form.cleaned_data['home'], form.cleaned_data['user']),
                    'shell=%s' % dict(form.fields['shell'].choices)[form.cleaned_data['shell']]]
        }
        print data
        salt = SaltApi()
        salt.get_token()
        header = salt.get_header()
        context = process(header, **data)
        if regex_match_error(context):
            status = True
        else:
            status = False
        new_form = form.save(commit=False)
        new_form.context = context
        new_form.status = status
        new_form.operate = request.session['username']
        new_form.home = os.path.join(form.cleaned_data['home'], form.cleaned_data['user'])
        new_form.save()
        form.save()
        for item in form.cleaned_data['tgt']:
            # print form.cleaned_data['user']
            user_info = SysUser.objects.filter(sys_user=form.cleaned_data['user'])
            if not user_info:
                user_object = SysUser(sys_user=form.cleaned_data['user'], servers_id=item.id)
                user_object.save()
                # get_sys_user = SysUser.objects.get(sys_user=form.cleaned_data['user'])
                # Assets.objects.filter(host_name=item.host_name).update(sys_users=get_sys_user)
            else:
                return HttpResponse("user already exist.")
                # get_sys_user = SysUser.objects.get(sys_user=form.cleaned_data['user'], servers=item)
                # Assets.objects.filter(host_name=item.host_name).update(sys_users=get_sys_user)

        return redirect('system_user_list')

    return render(request, template_name, {'form': form,
                                           'username': request.session['username'],
                                           'var7': 'active',
                                           'highlight8': 'active'})


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.delete_systemusermanager', raise_exception=True)
def system_user_del(request, template_name='saltstack/system_user_form.html'):
    form = SystemUserDelForm(request.POST or None)
    hosts = []
    if form.is_valid():
        for item in form.cleaned_data['tgt']:
            hosts.append(item.host_name)

        data = {
            'expr_form': 'list',
            'client': form.cleaned_data['client'],
            'tgt': hosts,
            'fun': form.cleaned_data['fun'],
            'arg': [form.cleaned_data['user'], 'remove=True', 'force=True']
        }
        print data
        salt = SaltApi()
        salt.get_token()
        header = salt.get_header()
        context = process(header, **data)
        print context
        if regex_match_error(context):
            status = True
        else:
            status = False
        new_form = form.save(commit=False)
        new_form.context = context
        new_form.status = status
        new_form.operate = request.session['username']
        new_form.home = os.path.join(form.cleaned_data['home'], form.cleaned_data['user'])
        new_form.save()
        form.save()
        for item in form.cleaned_data['tgt']:
            # server_info = Assets.objects.get(host_name=item.host_name)
            # server_info.sys_users.remove(SysUser.objects.get(sys_user=form.cleaned_data['user']))
            SysUser.objects.filter(servers_id=item.id, sys_user=form.cleaned_data['user']).delete()

        return redirect('system_user_list')

    return render(request, template_name, {'form': form,
                                           'username': request.session['username'],
                                           'var7': 'active',
                                           'highlight8': 'active'})


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.view_systemusermanager', raise_exception=True)
def system_user_operate_detail(request, pk, template_name='saltstack/system_user_detail.html'):
    try:
        details = SystemUserManager.objects.get(pk=pk)
    except SystemUserManager.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight8': 'active'
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.delete_systemusermanager', raise_exception=True)
def system_user_operation_history_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(SystemUserManager, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')
