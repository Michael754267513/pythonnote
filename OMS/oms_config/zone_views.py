# --*-- coding: utf-8 --*--

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from s.models import
from models import Zone
from forms import ZoneForm, ZoneEditForm


# Create your views here.


@login_required
@permission_required('Zone.view_zone', raise_exception=True)
def game_zone_list(request, template_name='oms_config/game_zone_list.html'):
    username = request.session['username']
    zones = Zone.objects.all()
    highlight1 = 'active'
    var4 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('Zone.add_zone', raise_exception=True)
def game_zone_add(request, template_name='oms_config/game_zone_add.html'):
    s = .objects.all()
    form = ZoneForm(request.POST or None)
    username = request.session['username']
    if form.is_valid():
        print form
        form.save()
        return redirect('game_zone_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var4': 'active',
                                           'highlight1': 'active',
                                           's': s})


@login_required
@permission_required('Zone.change_zone', raise_exception=True)
def game_zone_edit(request, pk, template_name='oms_config/game_zone_add.html'):
    username = request.session['username']
    zones = get_object_or_404(Zone, pk=pk)
    select = zones.s
    s = .objects.all()
    form = ZoneEditForm(request.POST or None, instance=zones)
    if form.is_valid():
        form.save()
        return redirect('game_zone_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var4': 'active',
                                           'highlight1': 'active',
                                           'select': select,
                                           's': s,
                                           'zones': zones,
                                           })


@login_required
@permission_required('Zone.delete_zone', raise_exception=True)
def game_zone_del(request):
    pk = request.GET['id']
    zones = get_object_or_404(Zone, pk=int(pk))
    zones.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('Zone.view_zone', raise_exception=True)
def game_zone_detail(request, pk, template_name='oms_config/game_zone_detail.html'):
    try:
        zones = Zone.objects.get(pk=pk)
    except Zone.DoesNotExist:
        raise Http404
    return render(request, template_name, {'zones': zones,
                                           'var4': 'active',
                                           'username': request.session['username'],
                                           'highlight1': 'active',
                                           })

