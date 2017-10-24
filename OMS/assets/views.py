# -*- coding:utf8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponse, Http404
from models import Assets, Hardware, Network, Services, Tag, SysUser
from forms import AssetsForm, HardwareForm, NetworkForm, ServicesForm, TagForm, AssetsEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
# from django.db.models.signals import post_delete
# from django.dispatch import receiver
from saltstack.models import SaltKey
import json


@login_required
@permission_required('Assets.view_network', raise_exception=True)
def network_list(request, template_name='assets/network_list.html'):
    username = request.session['username']
    networks = Network.objects.all()
    highlight3 = 'active'
    var5 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('Assets.add_network', raise_exception=True)
def network_add(request, template_name='assets/network_add.html'):
    form = NetworkForm(request.POST or None)
    username = request.session['username']
    if form.is_valid():
        form.save()
        return redirect('network_list')

    return render(request, template_name, {'form': form,
                                           'var5': 'active',
                                           'username': username,
                                           'highlight3': 'active'
                                           })


@login_required
@permission_required('Assets.change_network', raise_exception=True)
def network_edit(request, pk,  template_name='assets/network_add.html'):
    network = get_object_or_404(Network, pk=pk)
    username = request.session['username']
    form = NetworkForm(request.POST or None, instance=network)
    if form.is_valid():
        form.save()
        return redirect('network_list')

    return render(request, template_name, {'form': form,
                                           'var5': 'active',
                                           'username': username,
                                           'highlight3': 'active'})


@login_required
@permission_required('Assets.delete_network', raise_exception=True)
def network_del(request):
    pk = request.GET['id']
    network = get_object_or_404(Network, pk=int(pk))
    network.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('Assets.view_assets', raise_exception=True)
def assets_list(request, template_name='assets/assets_list.html'):
    username = request.session['username']
    assets = Assets.objects.filter(is_online=True)
    var5 = 'active'
    highlight1 = 'active'

    return render(request, template_name, locals())


@login_required
@permission_required('Assets.add_assets', raise_exception=True)
def assets_add(request, template_name='assets/assets_add.html'):
    username = request.session['username']
    if request.method == 'POST':
        form = AssetsForm(request.POST or None)
        networks_id = request.POST['networks']
        if form.is_valid():
            Network.objects.filter(id=networks_id).update(bind=1)
            form.save()
            return redirect('assets_list')
    else:
        form = AssetsForm()

    return render(request, template_name, {'form': form,
                                           'var5': 'active',
                                           'username': username,
                                           'highlight1': 'active'
                                           })


@login_required
@permission_required('Assets.change_assets', raise_exception=True)
def assets_edit(request, pk,  template_name='assets/assets_add.html'):
    assets = get_object_or_404(Assets, pk=pk)
    username = request.session['username']
    form = AssetsEditForm(request.POST or None, instance=assets)
    if form.is_valid():
        form.save()
        return redirect('assets_list')

    return render(request, template_name, {'form': form,
                                           'var5': 'active',
                                           'username': username
                                           })


@login_required
@permission_required('Assets.delete_assets', raise_exception=True)
def assets_delete(request):
    pk = request.GET['id']
    assets = get_object_or_404(Assets, pk=pk)
    assets.delete()
    Network.objects.filter(id=assets.networks_id).update(bind=0)
    return HttpResponse('delete success')


@login_required
@permission_required('Assets.view_assets', raise_exception=True)
def assets_detail(request, pk, template_name='assets/assets_detail.html'):
    try:
        assets = get_object_or_404(Assets, pk=pk)
        print SysUser.objects.filter(servers_id=pk)
        if SysUser.objects.filter(servers_id=pk):
            users = SysUser.objects.get(servers_id=pk)
        else:
            users = False
    except Assets.DoesNotExist:
        raise Http404
    return render(request, template_name, {'assets': assets,
                                           'var5': 'active',
                                           'highlight1': 'active',
                                           'username': request.session['username'],
                                           'users': users,
                                           })


@login_required
@permission_required('Assets.view_hardware', raise_exception=True)
def hardware_list(request, template_name='assets/hardware_list.html'):
    username = request.session['username']
    hardware = Hardware.objects.all()
    highlight2 = 'active'
    var5 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('Assets.add_hardware', raise_exception=True)
def hardware_add(request, template_name='assets/hardware_add.html'):
    form = HardwareForm(request.POST or None)
    username = request.session['username']
    if form.is_valid():
        form.save()
        return redirect('hardware_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var5': 'active',
                                           'highlight2': 'active'})


@login_required
@permission_required('Assets.change_hardware', raise_exception=True)
def hardware_edit(request, pk, template_name='assets/hardware_add.html'):
    username = request.session['username']
    hardware = get_object_or_404(Hardware, pk=pk)
    form = HardwareForm(request.POST or None, instance=hardware)
    if form.is_valid():
        form.save()
        return redirect('hardware_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var5': 'active',
                                           'highlight1': 'active',
                                           })


@login_required
@permission_required('Assets.delete_hardware', raise_exception=True)
def hardware_del(request):
    pk = request.GET['id']
    hardware = get_object_or_404(Hardware, pk=int(pk))
    hardware.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('Assets.view_services', raise_exception=True)
def service_list(request, template_name='assets/services_list.html'):
    username = request.session['username']
    services = Services.objects.all()
    var5 = 'active'
    highlight4 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('Assets.view_services', raise_exception=True)
def service_add(request, template_name='assets/services_add.html'):
    username = request.session['username']
    if request.method == 'POST':
        form = ServicesForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServicesForm

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var5': 'active',
                                           'highlight4': 'active',
                                           })


@login_required
@permission_required('Assets.chang_services', raise_exception=True)
def service_edit(request, pk, template_name='assets/services_add.html'):
    services = get_object_or_404(Services, pk=pk)
    username = request.session['username']
    form = ServicesForm(request.POST or None, instance=services)
    if form.is_valid():
        form.save()
        return redirect('service_list')

    return render(request, template_name, {'form': form,
                                           'services': services,
                                           'username': username,
                                           'var5': 'active',
                                           'highlight4': 'active'
                                           })


@login_required
@permission_required('Assets.delete_services', raise_exception=True)
def service_delete(request):
    pk = request.GET['id']
    services = get_object_or_404(Services, pk=int(pk))
    services.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('Assets.view_tag', raise_exception=True)
def tag_list(request, template_name='assets/tag_list.html'):
    username = request.session['username']
    tags = Tag.objects.all()
    var5 = 'active'
    highlight5 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('Assets.add_tag', raise_exception=True)
def tag_add(request, template_name='assets/tag_add.html'):
    username = request.session['username']
    if request.method == 'POST':
        form = TagForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var5': 'active',
                                           'highlight5': 'active',
                                           })


@login_required
@permission_required('Assets.view_tag', raise_exception=True)
def tag_edit(request, pk, template_name='assets/tag_add.html'):
    tags = get_object_or_404(Tag, pk=pk)
    username = request.session['username']
    form = TagForm(request.POST or None, instance=tags)
    if form.is_valid():
        form.save()
        return redirect('tag_list')

    return render(request, template_name, {'form': form,
                                           'tags': tags,
                                           'username': username,
                                           'var5': 'active',
                                           'highlight5': 'active',
                                           })


@login_required
@permission_required('Assets.delete_tag', raise_exception=True)
def tag_delete(request):
    pk = request.GET['id']
    tags = get_object_or_404(Tag, pk=int(pk))
    tags.delete()
    return HttpResponse('delete success')


@login_required
def make_server_offline(request, server):
    Assets.objects.filter(alias_name__contains=server).update(on_line=False)
    return redirect('dashboard')


@login_required
def make_server_online(request, server):
    Assets.objects.filter(host_name=server).update(is_online=True)
    return redirect('dashboard')


@login_required
def delete_assets_and_networks_from_database(request, server):
    global private_ip
    result = Assets.objects.filter(host_name=server)
    for item in result:
        # print item.networks.private_address
        private_ip = item.networks.private_address
        print private_ip
    Network.objects.filter(private_address=private_ip).delete()
    SaltKey.objects.filter(minion=server).update(is_getinfo=0)

    return redirect('dashboard')


@login_required
def get_servers(request, pk, template_name='assets/get_servers.html'):
    username = request.session['username']
    data = {}
    servers = Assets.objects.filter(game_zone__exact=pk)

    for item in servers:
        data['%s' % item.id] = '%s | %s' % (item.alias_name, item.host_name)
    result = json.dumps(data, encoding='UTF-8', ensure_ascii=False)

    return render(request, template_name, {'result': result, 'username': username})
