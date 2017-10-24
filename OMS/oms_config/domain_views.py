from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from s.models import
from models import Zone
from models import Domain
from forms import DomainForm


# Create your views here.


@login_required
@permission_required('oms_config.view_domain', raise_exception=True)
def domain_list(request, template_name='oms_config/domain_list.html'):
    username = request.session['username']
    domain_object = Domain.objects.all()
    highlight6 = 'active'
    var4 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('oms_config.add_domain', raise_exception=True)
def domain_add(request, template_name='oms_config/domain_add.html'):
    form = DomainForm(request.POST or None)
    s = .objects.all()
    zones = Zone.objects.all()
    username = request.session['username']
    if form.is_valid():
        print form
        form.save()
        return redirect('domain_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var4': 'active',
                                           'highlight6': 'active',
                                           's': s,
                                           'zones': zones,
                                           })


@login_required
@permission_required('oms_config.change_domain', raise_exception=True)
def domain_edit(request, pk, template_name='oms_config/domain_add.html'):
    username = request.session['username']
    domain_object = get_object_or_404(Domain, pk=pk)
    s = .objects.filter(id=domain_object.s.id)
    zones = Zone.objects.filter(id=domain_object.zones.id)
    form = DomainForm(request.POST or None, instance=domain_object)
    # print form
    if form.is_valid():
        # print form
        form.save()
        return redirect('domain_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var4': 'active',
                                           'highlight6': 'active',
                                           'domain_object': domain_object,
                                           's': s,
                                           'zones': zones,
                                           })


@login_required
@permission_required('oms_config.delete_domain', raise_exception=True)
def domain_del(request):
    pk = request.GET['id']
    objects = get_object_or_404(Domain, pk=int(pk))
    objects.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('oms_config.view_domain', raise_exception=True)
def domain_detail(request, pk, template_name='oms_config/domain_detail.html'):
    try:
        objects = Domain.objects.get(pk=pk)
    except Domain.DoesNotExist:
        raise Http404
    return render(request, template_name, {'objects': objects,
                                           'var4': 'active',
                                           'username': request.session['username'],
                                           'highlight6': 'active',
                                           })
