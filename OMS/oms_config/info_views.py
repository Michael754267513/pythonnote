# --*-- coding: utf-8 --*--

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from s.models import
from models import Information, Zone
from forms import InformationForm
import json


# Create your views here.


@login_required
@permission_required('Information.view_information', raise_exception=True)
def info_list(request, template_name='oms_config/information_list.html'):
    var4 = 'active'
    highlight2 = 'active'
    s = .objects.all()
    username = request.session['username']
    if request.method == 'POST':
        zone_id = int(request.POST['game_zone'])
        dep_id = int(request.POST['s'])
        info = Information.objects.filter(zones=zone_id)
        current_ = .objects.get(pk=dep_id)
        current_game_zone = Zone.objects.get(pk=zone_id)
    else:
        zones = Zone.objects.all()
        info = Information.objects.all()

    return render(request, template_name, locals())


@login_required
@permission_required('Information.add_information', raise_exception=True)
def info_add(request, template_name='oms_config/information_add.html'):
    form = InformationForm(request.POST or None)
    zones = Zone.objects.all()
    username = request.session['username']
    if form.is_valid():
        print form
        form.save()
        return redirect('info_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var4': 'active',
                                           'highlight2': 'active',
                                           'zones': zones,
                                           })


@login_required
@permission_required('Information.change_information', raise_exception=True)
def info_edit(request, pk, template_name='oms_config/information_add.html'):
    username = request.session['username']
    info = get_object_or_404(Information, pk=pk)
    select = info.zones
    zones = Zone.objects.all()
    form = InformationForm(request.POST or None, instance=info)
    if form.is_valid():
        form.save()
        return redirect('info_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var4': 'active',
                                           'highlight2': 'active',
                                           'zones': zones,
                                           'info': info,
                                           'select': select,
                                           })


@login_required
@permission_required('Information.delete_information', raise_exception=True)
def info_del(request):
    pk = request.GET['id']
    info = get_object_or_404(Information, pk=int(pk))
    info.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('Information.view_information', raise_exception=True)
def info_detail(request, pk, template_name='oms_config/information_detail.html'):
    try:
        info = Information.objects.get(pk=pk)
    except Information.DoesNotExist:
        raise Http404
    return render(request, template_name, {'info': info,
                                           'var4': 'active',
                                           'username': request.session['username'],
                                           'highlight2': 'active',
                                           })


@login_required
@permission_required('Information.view_information', raise_exception=True)
def game_zone_copy(request):
    pk = request.GET['id']
    pk2 = request.GET['id2']
    # print pk, pk2
    info = Information.objects.filter(zones=pk)
    # print info
    for item in info:
        item.id = None
        item.zones_id = pk2
        item.value = 'copy of ' + item.value
        item.save()

    return redirect('info_list')


@login_required
def get_zones(request, pk, template_name='oms_config/get_zones.html'):
    username = request.session['username']
    data = {}
    zone = {}
    zones = Zone.objects.filter(s_id=pk)
    for item in zones:
        zone['%s' % item.id] = item.name
    data['zone'] = zone
    result = json.dumps(data, encoding='UTF-8', ensure_ascii=False)

    return render(request, template_name, {'result': result,
                                           'username': username,
                                           })
