# --*-- coding: utf-8 --*--

import json
import string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404, get_object_or_404, HttpResponse
from s.models import
from assets.models import Assets, SysUser
from forms import PasswordFrom
from models import Password
from saltstack.scripts.generate_random_string import gen_random_string
from saltstack.scripts.re_match_result import regex_match_error
from saltstack.scripts.salt_api import *


# Create your views here.


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.view_password', raise_exception=True)
def change_password_record(request, template_name='saltstack/change_sys_password_record.html'):
    username = request.session['username']
    password_object = Password.objects.all()
    highlight9 = 'active'
    var7 = 'active'

    return render(request, template_name, locals())


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.add_password', raise_exception=True)
def change_sys_password(request, template_name='saltstack/change_sys_password_process.html'):
    s = .objects.all()
    tgt = Assets.objects.filter(is_online=True)
    form = PasswordFrom(request.POST or None)
    gen_string = {}
    hash_string = {}
    context = {}

    if form.is_valid():
        for item in form.cleaned_data['tgt']:
            password_charset = string.ascii_letters + string.digits
            gen_string['%s' % item.host_name] = gen_random_string(password_charset, 16)
            data = {
                'expr_form': 'list',
                'client': form.cleaned_data['client'],
                'tgt': item.host_name,
                'fun': 'shadow.gen_password',
                'arg': gen_string[item.host_name]
            }
            print data

            salt = SaltApi()
            salt.get_token()
            header = salt.get_header()
            result = change_password(header, **data)
            hash_string[item.host_name] = result[item.host_name]
            data = {
                'expr_form': 'list',
                'client': form.cleaned_data['client'],
                'tgt': item.host_name,
                'fun': 'shadow.set_password',
                'arg': [form.cleaned_data['user'], hash_string[item.host_name]]
            }
            print data

            context[item.host_name] = process(header, **data)

            if form.cleaned_data['user'] == 'root':
                Assets.objects.filter(host_name=item.host_name).update(superuser_pass=gen_string[item.host_name])
            else:
                SysUser.objects.filter(servers__host_name=item.host_name,
                                       sys_user=form.cleaned_data['user']).update(sys_pass=gen_string[item.host_name])
                # for assets in Assets.objects.filter(host_name=item.host_name):
                #     assets.sys_users.filter(sys_user=form.cleaned_data['user']).\
                #         update(sys_pass=gen_string[item.host_name])
        if regex_match_error(json.dumps(context)):
            status = True
        else:
            status = False
        new_form = form.save(commit=False)
        new_form.operate = request.session['username']
        new_form.status = status
        new_form.context = json.dumps(context)
        # new_form.context = context
        new_form.save()
        form.save()

        return redirect('change_password_record')

    return render(request, template_name, {'form': form,
                                           'var7': 'active',
                                           'highlight9': 'active',
                                           'username': request.session['username'],
                                           's': s,
                                           'tgt': tgt
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.view_password', raise_exception=True)
def change_password_detail(request, pk, template_name='saltstack/change_sys_password_detail.html'):
    try:
        details = Password.objects.get(pk=pk)
    except Password.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight9': 'active'
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.delete_password', raise_exception=True)
def change_password_record_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(Password, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')
