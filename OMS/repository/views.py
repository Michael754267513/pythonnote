# -*- coding:utf8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponse, Http404
from models import Repository, Version
from forms import RepositoryForm, VersionForm, LocalArchiveForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from saltstack.scripts.get_newVersion_from_gitLog import get_version
# from saltstack.scripts.create_folder import makedir_p
from saltstack.scripts.repo_process import *
# from saltstack.scripts.re_match_result import *
import os


@login_required(login_url='/accounts/login/')
@permission_required('repository.view_repository', raise_exception=True)
def repository_list(request, template_name='repository/repository_list.html'):
    username = request.session['username']
    repo_list = Repository.objects.all()
    var6 = 'active'
    highlight1 = 'active'
    return render(request, template_name, locals())


@login_required(login_url='/accounts/login/')
@permission_required('repository.add_repository', raise_exception=True)
def repository_add(request, template_name='repository/repository_add.html'):
    form = RepositoryForm(request.POST or None)
    username = request.session['username']
    var6 = 'active'
    if form.is_valid():
        form.save()
        return redirect('repository_list')

    return render(request, template_name, {'form': form,
                                           'var6': var6,
                                           'username': username,
                                           'highlight1': 'active',
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('repository.change_repository', raise_exception=True)
def repository_edit(request, pk,  template_name='repository/repository_add.html'):
    repository = get_object_or_404(Repository, pk=pk)
    username = request.session['username']
    form = RepositoryForm(request.POST or None, instance=repository)
    if form.is_valid():
        form.save()
        return redirect('repository_list')

    return render(request, template_name, {'form': form,
                                           'var6': 'active',
                                           'username': username,
                                           'repository': repository,
                                           'highlight1': 'active',
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('repository.delete_repository', raise_exception=True)
def repository_del(request):
    pk = request.GET['id']
    repository = get_object_or_404(Repository, pk=int(pk))
    repository.delete()
    return HttpResponse('delete success')


@login_required(login_url='/accounts/login/')
@permission_required('repository.view_assets', raise_exception=True)
def repository_detail(request, pk, template_name='repository/repository_detail.html'):
    try:
        repository = Repository.objects.get(pk=pk)
    except Repository.DoesNotExist:
        raise Http404
    return render(request, template_name, {'repository': repository,
                                           'var6': 'active',
                                           'username': request.session['username'],
                                           'highlight1': 'active',
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('repository.view_version', raise_exception=True)
def repo_version_list(request, template_name='repository/repo_version_list.html'):
    username = request.session['username']
    versions = Version.objects.all()
    var6 = 'active'
    highlight2 = 'active'
    return render(request, template_name, locals())


@login_required(login_url='/accounts/login/')
@permission_required('repository.add_version', raise_exception=True)
def repo_version_add(request, template_name='repository/repo_version_add.html'):
    form = VersionForm(request.POST or None)
    username = request.session['username']
    if form.is_valid():
        project_name = form.cleaned_data['repository'].repo_tag
        print project_name
        archive_path = os.path.join(form.cleaned_data['archive_path'], project_name)
        version = get_version(archive_path)
        if not version:
            return HttpResponse("Your configuration specifies to merge with the ref 'master' from the remote, "
                                "but no such ref was fetched.")
        if Version.objects.filter(version=version[0]):
            return HttpResponse("already exist.")
        else:
            version_object = Version(project=project_name, version=version[0], timestamp=version[1],
                                     author=version[2], content=version[3], vernier=u'0')
            version_object.save()

        return redirect('repo_version_list')

    return render(request, template_name, {'form': form,
                                           'var6': 'active',
                                           'username': username,
                                           'highlight2': 'active',
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('repository.delete_version', raise_exception=True)
def repo_version_del(request):
    pk = request.GET['id']
    print pk
    versions = get_object_or_404(Version, pk=int(pk))
    versions.delete()
    return HttpResponse('delete success')


@login_required(login_url='/accounts/login/')
@permission_required('repository.view_version', raise_exception=True)
def repo_version_detail(request, pk, template_name='repository/repo_version_detail.html'):
    try:
        versions = Version.objects.get(pk=pk)
    except Version.DoesNotExist:
        raise Http404
    return render(request, template_name, {'versions': versions,
                                           'var6': 'active',
                                           'username': request.session['username'],
                                           'highlight2': 'active',
                                           })


@login_required(login_url='/accounts/login/')
@permission_required('repository.view_version', raise_exception=True)
def local_archive_process(request, template_name='repository/local_archive_process.html'):
    form = LocalArchiveForm(request.POST or None)
    if form.is_valid():
        project = form.cleaned_data['repository'].repo_tag
        archive_path = form.cleaned_data['archive_path']
        repository = form.cleaned_data['repository']
        # print project
        # print archive_path
        # print repository.repo_user, repository.repo_pass, repository.repo_address

        # archive_abs_path = os.path.join(archive_path, project)
        # if not os.path.exists(archive_abs_path):
        #     makedir_p(archive_path)

        repository_url = get_repo_url(repository)
        content = git_checkout(archive_path, project, repository_url)
        if content:
            return redirect('repo_version_list')
        else:
            return HttpResponse("Failed")

    return render(request, template_name, {'form': form})
