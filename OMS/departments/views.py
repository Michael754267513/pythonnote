from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from models import
from forms import Form


# Create your views here.

@login_required
@permission_required('.view_', raise_exception=True)
def _list(request, template_name='s/_list.html'):
    username = request.session['username']
    deps = .objects.all()
    var3 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('.add_', raise_exception=True)
def _add(request, template_name='s/_add.html'):
    form = Form(request.POST or None)
    username = request.session['username']
    print username
    if form.is_valid():
        print form
        form.save()
        return redirect('_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var3': 'active',
                                           })


@login_required
@permission_required('.change_', raise_exception=True)
def _edit(request, pk, template_name='s/_add.html'):
    username = request.session['username']
    deps = get_object_or_404(, pk=pk)
    form = Form(request.POST or None, instance=deps)
    if form.is_valid():
        form.save()
        return redirect('_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var3': 'active',
                                           'deps': deps,
                                           })


@login_required
@permission_required('.delete_', raise_exception=True)
def _del(request):
    pk = request.GET['id']
    deps = get_object_or_404(, pk=int(pk))
    deps.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('.view_', raise_exception=True)
def _detail(request, pk, template_name='s/_detail.html'):
    try:
        deps = .objects.get(pk=pk)
    except .DoesNotExist:
        raise Http404
    return render(request, template_name, {'deps': deps,
                                           'var3': 'active',
                                           'username': request.session['username'],
                                           })
