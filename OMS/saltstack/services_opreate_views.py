# --*-- coding: utf-8 --*--

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404, get_object_or_404, HttpResponse

from assets.models import Assets, Services
from s.models import
from forms import ServicesHandleForm
from models import ServicesHandle
from oms_config.models import Zone
from saltstack.scripts.re_match_result import regex_match_error
from saltstack.scripts.salt_api import *


# Create your views here.


@login_required
@permission_required('saltstack.view_servicehandle', raise_exception=True)
def services_handle_list(request, template_name='saltstack/services_handle_list.html'):
    username = request.session['username']
    handles = ServicesHandle.objects.all()
    highlight4 = 'active'
    var7 = 'active'

    return render(request, template_name, locals())


# services handle

@login_required
@permission_required('Salt.add_serviceshandle', raise_exception=True)
def services_handle_process(request, template_name='saltstack/services_handle_form.html'):
    servers = Assets.objects.all()
    s = .objects.all()
    services = Services.objects.all()

    form = ServicesHandleForm(request.POST or None)
    if form.is_valid():
        data = {
            'expr_form': 'list',
            'client': form.cleaned_data['client'],
            'fun': form.cleaned_data['fun'],
            'tgt': [item.host_name for item in form.cleaned_data['tgt'].all()],
            'arg': form.cleaned_data['services'].name,
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
        new_form.context = context
        new_form.status = status
        new_form.operate = request.session['username']
        new_form.save()
        form.save()

        return redirect('services_handle_list')

    return render(request, template_name, {'highlight4': 'active',
                                           'username': request.session['username'],
                                           'form': form,
                                           'servers': servers,
                                           's': s,
                                           'services': services,
                                           'var7': 'active'
                                           })


@login_required
@permission_required('Salt.view_services_handle', raise_exception=True)
def services_handle_detail(request, pk, template_name='saltstack/services_handle_detail.html'):
    try:
        details = ServicesHandle.objects.get(pk=pk)
    except ServicesHandle.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight4': 'active'
                                           })


@login_required
@permission_required('Salt.delete_serviceshandle', raise_exception=True)
def services_handle_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(ServicesHandle, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')
