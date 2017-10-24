# --*-- coding: utf-8 --*--

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404, get_object_or_404, HttpResponse

from assets.models import Assets
from s.models import
from forms import CronForm
from models import Cron
from oms_config.models import Zone
from saltstack.scripts.re_match_result import regex_match_error
from saltstack.scripts.salt_api import *


# Create your views here.


@login_required
@permission_required('Salt.view_cron', raise_exception=True)
def cron_list(request, template_name='saltstack/cron_list.html'):
    username = request.session['username']
    cron_object = Cron.objects.all()
    var7 = 'active'
    highlight6 = 'active'

    return render(request, template_name, locals())


@login_required
@permission_required('Salt.add_cron', raise_exception=True)
def cron_jobs(request, template_name='saltstack/cron_form.html'):
    data = {}
    servers = Assets.objects.all()
    s = .objects.all()
    zones = Zone.objects.all()

    form = CronForm(request.POST or None)
    if form.is_valid():
        # print form
        if form.cleaned_data['fun'] == 'cron.rm_job':
            data = {
                'expr_form': 'list',
                'client': form.cleaned_data['client'],
                'fun': form.cleaned_data['fun'],
                'tgt': [item.host_name for item in form.cleaned_data['tgt'].all()],
                'arg': [form.cleaned_data['sys_user'],
                        form.cleaned_data['arg']]
            }

        if form.cleaned_data['fun'] == 'cron.set_job':
            data = {
                'expr_form': 'list',
                'client': form.cleaned_data['client'],
                'fun': form.cleaned_data['fun'],
                'tgt': [item.host_name for item in form.cleaned_data['tgt'].all()],
                'arg': [form.cleaned_data['sys_user'],
                        form.cleaned_data['minute'],
                        form.cleaned_data['hour'],
                        form.cleaned_data['day'],
                        form.cleaned_data['month'],
                        form.cleaned_data['day_week'],
                        form.cleaned_data['arg']]
            }

        if form.cleaned_data['fun'] == 'cron.raw_cron':
            data = {
                'expr_form': 'list',
                'client': form.cleaned_data['client'],
                'fun': form.cleaned_data['fun'],
                'tgt': [item.host_name for item in form.cleaned_data['tgt'].all()],
                'arg': [form.cleaned_data['sys_user']]
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
        new_form.operate = request.session['username']
        new_form.status = status
        new_form.save()
        form.save()

        return redirect('cron_list')

    return render(request, template_name, {'highlight6': 'active',
                                           'username': request.session['username'],
                                           'form': form,
                                           'servers': servers,
                                           'zones': zones,
                                           's': s,
                                           'var7': 'active'
                                           })


@login_required
@permission_required('Salt.view_cron', raise_exception=True)
def cron_detail(request, pk, template_name='saltstack/cron_detail.html'):
    try:
        details = Cron.objects.get(pk=pk)
    except Cron.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight6': 'active'
                                           })


@login_required
@permission_required('Salt.delete_cron', raise_exception=True)
def cron_history_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(Cron, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')
