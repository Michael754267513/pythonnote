# --*-- coding: utf-8 --*--

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404, get_object_or_404, HttpResponse
# from OMS.settings import GENERATE_URL, SCRIPT_URL, CONF_URL
from assets.models import Assets
from s.models import
from forms import PushForm, Unix2DosForm
from models import Push
from oms_config.models import Produce, Zone
from p2p_scp_views import logging_out
from saltstack.scripts.re_match_result import regex_match_error
from scripts.salt_api import *
from scripts.create_folder import makedir_p
from scripts.execute_command import running_command


@login_required
@permission_required('saltstack.view_push', raise_exception=True)
def push_list(request, template_name='saltstack/file_push_list.html'):
    username = request.session['username']
    file_copies = Push.objects.all()
    highlight3 = 'active'
    var7 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('saltstack.add_push', raise_exception=True)
def push_process(request, template_name='saltstack/file_push_form.html'):
    form = PushForm(request.POST or None)
    servers = Assets.objects.all().order_by('alias_name')
    s = .objects.all()
    zones = Zone.objects.all()
    files = Produce.objects.all()

    if form.is_valid():
        #  = form.cleaned_data['s'].name
        zone = form.cleaned_data['zones'].name
        domain = form.cleaned_data['domains'].name
        service = form.cleaned_data['service_name']
        service_name = dict(form.fields['service_name'].choices)[service]
        file_name = form.cleaned_data['file_name']
        source_path = form.cleaned_data['source_path']
        target_path = form.cleaned_data['target_path'].path_value
        generate_file = zone + '_' + file_name
        conf_templates_path = os.path.join('/srv/salt/service_config/templates', service_name)
        conf_generate_path = os.path.join('/srv/salt/service_config/', zone, service_name)

        if not os.path.exists(conf_generate_path):
            makedir_p(conf_generate_path)

        commands = "sh /data/deploy/OMS/saltstack/scripts/shell/replace_service_conf.sh %s %s %s %s %s %s" % \
                   (file_name, generate_file, domain, zone, conf_templates_path, conf_generate_path)

        # 生成新配置文件
        running_command(commands)

        salt_file_storage = os.path.join(source_path, zone, service_name, generate_file)
        print salt_file_storage
        target_abs_path = os.path.join(target_path, generate_file)
        print target_abs_path

        template = 'jinja'
        env = 'base'
        makedirs = False

        data = {
            'expr_form': 'list',
            'client': form.cleaned_data['client'],
            'fun': 'cp.get_template',
            'tgt': [item.host_name for item in form.cleaned_data['tgt'].all()],
            'arg': [salt_file_storage, target_abs_path, template, env, makedirs],
        }
        print data
        salt = SaltApi()
        salt.get_token()
        header = salt.get_header()
        context = process(header, **data)
        print context
        if regex_match_error(context):
            status = True
        else:
            status = False
        print status

        new_form = form.save(commit=False)
        new_form.context = context
        new_form.source_path = salt_file_storage
        new_form.file_name = target_abs_path
        new_form.status = status
        new_form.operate = request.session['username']
        new_form.save()
        form.save()

        return redirect('file_push_list')

    return render(request, template_name, {'highlight3': 'active',
                                           'username': request.session['username'],
                                           'form': form,
                                           'servers': servers,
                                           's': s,
                                           'zones': zones,
                                           'files': files,
                                           'var7': 'active',
                                           })


@login_required
@permission_required('saltstack.view_push', raise_exception=True)
def push_detail(request, pk, template_name='saltstack/file_push_detail.html'):
    try:
        details = Push.objects.get(pk=pk)
    except Push.DoesNotExist:
        raise Http404
    return render(request, template_name, {'details': details,
                                           'var7': 'active',
                                           'username': request.session['username'],
                                           'highlight3': 'active'
                                           })


@login_required
@permission_required('saltstack.delete_push', raise_exception=True)
def push_history_del(request):
    pk = request.GET['id']
    histories = get_object_or_404(Push, pk=int(pk))
    histories.delete()
    return HttpResponse('delete success')


@login_required(login_url='/accounts/login/')
@permission_required('saltstack.add_push', raise_exception=True)
def unix2dos(request, template_name='saltstack/unix2dos.html'):
    form = Unix2DosForm(request.POST or None)
    if form.is_valid():
        abs_path_file = form.cleaned_data['file']
        command = 'unix2dos %s' % abs_path_file
        data = {
            'expr_form': 'list',
            'client': 'local',
            'fun': 'cmd.run',
            'tgt': form.cleaned_data['tgt'],
            'arg': command,
        }
        print data
        salt = SaltApi()
        salt.get_token()
        header = salt.get_header()
        context = process(header, **data)
        html = "<html><body><pre>%s</pre></body></html>" % context
        logging_out(context)
        return HttpResponse(html)

    return render(request, template_name, {'form': form,
                                           'var7': 'active',
                                           'highlight3': 'active',
                                           'username': request.session['username']})
