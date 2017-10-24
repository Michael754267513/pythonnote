# --*-- coding: utf-8 --*--

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404, get_object_or_404, HttpResponse
from assets.models import Assets
from s.models import
from forms import ReleaseForm
from models import Release, RELEASE_FUN_CHOICES
from oms_config.models import Path
from oms_config.models import Zone
from repository.models import Repository
# from repository.models import Version
from saltstack.scripts.salt_api import *
from saltstack.scripts.re_match_result import regex_match_error
# from django.db.models import Q


@login_required
@permission_required('Salt.view_release', raise_exception=True)
def code_release_list(request, template_name='saltstack/code_release_list.html'):
    username = request.session['username']
    release_list = Release.objects.all()
    highlight2 = 'active'
    var7 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('Salt.add_release', raise_exception=True)
def code_release(request, template_name='saltstack/code_release_form.html'):
    form = ReleaseForm(request.POST or None)
    servers = Assets.objects.all()
    s = .objects.all()
    zones = Zone.objects.all()
    repo = Repository.objects.all()
    deploy_path = Path.objects.all()
    global status

    if form.is_valid():
        repo_name = form.cleaned_data['repository_name']
        result = Repository.objects.filter(repo_name__contains=repo_name)[0]
        if result.repo_protocol == '3':
            repository_url = 'https://%s:%s@%s' % (result.repo_user, result.repo_pass, result.repo_address)
        elif result.repo_protocol == '2':
            repository_url = 'http://%s:%s@%s' % (result.repo_user, result.repo_pass, result.repo_address)
        else:
            repository_url = '%s@%s' % (result.repo_user, result.repo_address)

        project_name = form.cleaned_data['repository_name'].repo_tag
        zone_name = form.cleaned_data['zones'].name
        deploy_path = form.cleaned_data['deploy_path'].path_value
        release_path = form.cleaned_data['release_path'].path_value
        # versions = form.cleaned_data['versions']
        # version = versions.version
        # version_id = versions.id
        print project_name, zone_name, release_path

        if form.cleaned_data['use_zone']:
            deploy_abs_path = os.path.join(deploy_path, (project_name + '_' + zone_name))
            release_abs_path = release_path + '_' + zone_name
        else:
            deploy_abs_path = os.path.join(deploy_path, project_name)
            release_abs_path = release_path

        fun_value = dict(RELEASE_FUN_CHOICES).get(form.cleaned_data['fun'])

        data = {
            'expr_form': 'list',
            'client': form.cleaned_data['client'],
            'tgt': [item.host_name for item in form.cleaned_data['tgt']],
            'fun': fun_value,
            'arg': [deploy_abs_path, repository_url],
        }
        print data
        salt = SaltApi()
        salt.get_token()
        header = salt.get_header()
        context = process(header, **data)
        print context

        if form.cleaned_data['fun'] == u'1':
            shell = 'rm -rf %s && ln -s %s %s' % (release_abs_path, deploy_abs_path, release_abs_path)
            data = {
                'expr_form': 'list',
                'client': form.cleaned_data['client'],
                'tgt': [item.host_name for item in form.cleaned_data['tgt']],
                'fun': 'cmd.run',
                'arg': shell,
            }
            # print data
            release_context = process(header, **data)
        else:
            release_context = "symlink not change."

        for item in form.cleaned_data['tgt']:
            result = yaml.load(context)['return'][0][item.host_name]
            if result is True or result == "Already up-to-date." and regex_match_error(release_context) is True:
                status = True
            else:
                status = False
        new_form = form.save(commit=False)
        new_form.context = context
        new_form.deploy_path = deploy_abs_path
        new_form.release_path = release_abs_path
        new_form.operate = request.session['username']
        new_form.status = status
        new_form.save()
        form.save()
        return redirect('code_release_list')

    return render(request, template_name, {'highlight2': 'active',
                                           'username': request.session['username'],
                                           'form': form,
                                           'servers': servers,
                                           's': s,
                                           'zones': zones,
                                           'deploy_path': deploy_path,
                                           'repo': repo,
                                           'var7': 'active',
                                           })


@login_required
@permission_required('Salt.view_release', raise_exception=True)
def code_release_detail(request, pk, template_name='saltstack/code_release_detail.html'):
    try:
        details = Release.objects.get(pk=pk)
    except Release.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight2': 'active'
                                           })


@login_required
@permission_required('Salt.delete_release', raise_exception=True)
def code_release_history_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(Release, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')
