# --*-- coding: utf-8 --*--

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from s.models import
# from repository.models import Repository
from models import Upload
from forms import UploadForm
from saltstack.scripts.create_folder import makedir_p
# from django.template import RequestContext
import os


# Create your views here.


@login_required
@permission_required('oms_config.view_upload', raise_exception=True)
def upload_file_list(request, template_name='oms_config/upload_list.html'):
    username = request.session['username']
    var4 = 'active'
    highlight3 = 'active'
    files = Upload.objects.all()

    return render(request, template_name, locals())


@login_required
@permission_required('oms_config.add_upload', raise_exception=True)
def file_upload(request, template_name='oms_config/file_upload_form.html'):
    var4 = 'active'
    s = .objects.all()
    # repository = Repository.objects.all()
    username = request.session['username']
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # print form
            new_file = Upload(
                doc_file=request.FILES['doc_file'],
                s_id=request.POST['s'],
                title=request.POST['title']
            )
            new_file.save()
            # handle_uploaded_file(request.FILES['file'])
            return redirect('upload_list')
    else:
        form = UploadForm()

    return render(request, template_name, {'form': form,
                                           'var4': var4,
                                           'username': username,
                                           'highlight3': 'active',
                                           's': s,
                                           })


@login_required
@permission_required('oms_config.add_upload', raise_exception=True)
def multi_file_upload(request, template_name='oms_config/file_upload_form.html'):
    s = .objects.all()
    # repository = Repository.objects.all()
    username = request.session['username']
    form = UploadForm(request.POST, request.FILES)

    # if request.method == 'POST':
    #     if form.is_valid():
    #         # print form
    #         # project_name = form.cleaned_data['repository_name'].repo_tag
    #         # upload_path = os.path.join("/data/deploy/OMS/media/Upload", project_name)
    #         # print upload_path
    #         # files = request.FILES.getlist("doc_file")
    #         files = request.FILES.getlist("doc_file")
    #         for item in files:
    #             print item.name
    #             # new_file = Upload(doc_file=item.name,
    #             #                   s_id=request.POST['s'],
    #             #                   title=request.POST['title'])
    #             # new_file.save()
    #             handle_uploaded_file(item)
    #         # form.save()
    #         # return redirect('upload_list')
    #             return HttpResponse("File(s) uploaded!")
    # else:
    #     form = UploadForm()

    return render(request, template_name, {'form': form,
                                           'var4': 'active',
                                           'username': username,
                                           'highlight3': 'active',
                                           's': s,
                                           })


def upload_action(request):

    upload_path = '/data/deploy/OMS/media/Upload'
    files = request.FILES.getlist('doc_file')
    for item in files:
        if not os.path.exists(upload_path):
            makedir_p(upload_path)

        def handle_uploaded_file(f):
            with open(upload_path + '/' + f.name, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        handle_uploaded_file(item)

        uploads = Upload(
            doc_file=os.path.join(upload_path, item.name),
            s_id=request.POST['s'],
            title=request.POST['title']
            )
        uploads.save()

    return HttpResponse("File(s) uploaded!")


@login_required
@permission_required('Games.delete_upload', raise_exception=True)
def upload_del(request):
    pk = request.GET['id']
    files = get_object_or_404(Upload, pk=int(pk))
    files.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('oms_config.view_upload', raise_exception=True)
def show_files(request, pk, template_name='oms_config/show_files.html'):
    global doc_title
    global doc_name
    global doc_content
    global doc_
    print request.session['username']
    objects = Upload.objects.filter(id=pk)
    for item in objects:
        doc_ = item.s.name
        doc_title = item.title
        doc_name = item.doc_file.name
        doc_content = item.display_text_file()

    return render(request, template_name, {'objects': objects,
                                           'var4': 'active',
                                           'highlight3': 'active',
                                           'username': request.session['username'],
                                           'doc_title': doc_title,
                                           'doc_name': doc_name,
                                           'doc_content': doc_content,
                                           'doc_': doc_
                                           },)
