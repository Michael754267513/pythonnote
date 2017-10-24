# --*-- coding: utf-8 --*--

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404, get_object_or_404, HttpResponse
from assets.models import Assets
from s.models import
from forms import ExecuteCommandForm
from models import ExecuteCommand
from oms_config.models import Zone
from saltstack.scripts.re_match_result import regex_match_error
from saltstack.scripts.salt_api import *


# Create your views here.


@login_required
@permission_required('Salt.view_execute_command', raise_exception=True)
def command_execute_list(request, template_name='saltstack/execute_command_list.html'):
    username = request.session['username']
    handles = ExecuteCommand.objects.all()
    highlight5 = 'active'
    var7 = 'active'

    return render(request, template_name, locals())


@login_required
@permission_required('Salt.add_executecommand', raise_exception=True)
def command_execute_process(request, template_name='saltstack/execute_command_form.html'):
    servers = Assets.objects.all()
    s = .objects.all()

    form = ExecuteCommandForm(request.POST or None)
    if form.is_valid():
        data = {
            'expr_form': 'list',
            'client': form.cleaned_data['client'],
            'fun': form.cleaned_data['fun'],
            'tgt': [item.host_name for item in form.cleaned_data['tgt'].all()],
            'arg': form.cleaned_data['commands'],
        }
        salt = SaltApi()
        salt.get_token()
        header = salt.get_header()
        context = process(header, **data)
        if regex_match_error(context):
            status = True
        else:
            status = False
        new_form = form.save(commit=False)
        new_form.operate = request.session['username']
        new_form.status = status
        new_form.context = context
        new_form.save()
        form.save()

        return redirect('command_execute_list')

    return render(request, template_name, {'highlight5': 'active',
                                           'username': request.session['username'],
                                           'form': form,
                                           'servers': servers,
                                           's': s,
                                           'var7': 'active'
                                           })


@login_required
@permission_required('Salt.view_executecommand', raise_exception=True)
def execute_command_detail(request, pk, template_name='saltstack/execute_command_detail.html'):
    try:
        details = ExecuteCommand.objects.get(pk=pk)
    except ExecuteCommand.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight5': 'active'
                                           })


@login_required
@permission_required('Salt.delete_executecommand', raise_exception=True)
def execute_history_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(ExecuteCommand, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')


