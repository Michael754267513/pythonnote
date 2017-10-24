from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from models import Redis
from forms import RedisForm
from s.models import
from oms_config.models import Zone

# Create your views here.


@login_required(login_url='/accounts/login/')
@permission_required('dbs_redis.view_redis', raise_exception=True)
def dbs_redis_list(request, template_name='dbs_redis/redis_list.html'):
    username = request.session['username']
    dbs = Redis.objects.all()
    highlight1 = 'active'
    var9 = 'active'
    return render(request, template_name, locals())


@login_required(login_url='/accounts/login/')
@permission_required('dbs_redis.add_redis', raise_exception=True)
def dbs_redis_add(request, template_name='dbs_redis/redis_add.html'):
    form = RedisForm(request.POST or None)
    s = .objects.all()
    zones = Zone.objects.all()
    username = request.session['username']
    if form.is_valid():
        form.save()
        return redirect('dbs_redis_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var9': 'active',
                                           'highlight1': 'active',
                                           's': s,
                                           'zones': zones,
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('dbs_redis.change_database', raise_exception=True)
def dbs_redis_edit(request, pk, template_name='dbs_redis/redis_add.html'):
    username = request.session['username']
    dbs = get_object_or_404(Redis, pk=pk)
    d_select = dbs.s
    s = .objects.all()
    form = RedisForm(request.POST or None, instance=dbs)
    if form.is_valid():
        form.save()
        return redirect('dbs_redis_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var9': 'active',
                                           'highlight1': 'active',
                                           'dbs': dbs,
                                           's': s,
                                           'd_select': d_select,
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('dbs_redis.delete_redis', raise_exception=True)
def dbs_redis_del(request):
    pk = request.GET['id']
    dbs = get_object_or_404(Redis, pk=int(pk))
    dbs.delete()
    return HttpResponse('delete success')


@login_required(login_url='/accounts/login/')
@permission_required('dbs_redis.view_redis', raise_exception=True)
def dbs_redis_detail(request, pk, template_name='dbs_redis/redis_detail.html'):
    try:
        dbs = Redis.objects.get(pk=pk)
    except Redis.DoesNotExist:
        raise Http404
    return render(request, template_name, {'dbs': dbs,
                                           'var9': 'active',
                                           'username': request.session['username'],
                                           'highlight1': 'active',
                                           })
