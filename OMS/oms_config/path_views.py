from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from s.models import
from models import Path
from forms import PathForm


# Create your views here.


@login_required
@permission_required('oms_config.view_path', raise_exception=True)
def path_list(request, template_name='oms_config/path_list.html'):
    username = request.session['username']
    path_object = Path.objects.all()
    highlight4 = 'active'
    var4 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('oms_config.add_path', raise_exception=True)
def path_add(request, template_name='oms_config/path_add.html'):
    form = PathForm(request.POST or None)
    s = .objects.all()
    username = request.session['username']
    if form.is_valid():
        print form
        form.save()
        return redirect('path_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var4': 'active',
                                           'highlight4': 'active',
                                           's': s,
                                           })


@login_required
@permission_required('oms_config.change_path', raise_exception=True)
def path_edit(request, pk, template_name='oms_config/path_add.html'):
    username = request.session['username']
    path_object = get_object_or_404(Path, pk=pk)
    select = path_object.s
    s = .objects.all()
    form = PathForm(request.POST or None, instance=path_object)
    if form.is_valid():
        form.save()
        return redirect('path_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var4': 'active',
                                           'highlight4': 'active',
                                           'path_object': path_object,
                                           's': s,
                                           'select': select,
                                           })


@login_required
@permission_required('oms_config.delete_path', raise_exception=True)
def path_del(request):
    pk = request.GET['id']
    path_object = get_object_or_404(Path, pk=int(pk))
    path_object.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('oms_config.view_path', raise_exception=True)
def path_detail(request, pk, template_name='oms_config/path_detail.html'):
    try:
        path_object = Path.objects.get(pk=pk)
    except Path.DoesNotExist:
        raise Http404
    return render(request, template_name, {'path_object': path_object,
                                           'var4': 'active',
                                           'username': request.session['username'],
                                           'highlight4': 'active',
                                           })
