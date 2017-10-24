from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from models import Databases
from forms import DatabasesForm
from s.models import
from oms_config.models import Zone
# from MySQLdb_api import MySQLUserProcess

# Create your views here.


@login_required
@permission_required('dbs_mysql.view_databases', raise_exception=True)
def database_list(request, template_name='databases/database_list.html'):
    username = request.session['username']
    dbs = Databases.objects.all()
    highlight1 = 'active'
    var8 = 'active'
    return render(request, template_name, locals())


@login_required
@permission_required('dbs_mysql.add_database', raise_exception=True)
def database_add(request, template_name='databases/database_add.html'):
    form = DatabasesForm(request.POST or None)
    s = .objects.all()
    zones = Zone.objects.all()
    username = request.session['username']
    if form.is_valid():
        form.save()
        return redirect('dbs_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var8': 'active',
                                           'highlight1': 'active',
                                           's': s,
                                           'zones': zones,
                                           })


@login_required
@permission_required('dbs_mysql.change_database', raise_exception=True)
def database_edit(request, pk, template_name='databases/database_add.html'):
    username = request.session['username']
    dbs = get_object_or_404(Databases, pk=pk)
    _select = dbs.s
    s = .objects.all()
    zones = Zone.objects.all()

    form = DatabasesForm(request.POST or None, instance=dbs)
    if form.is_valid():
        form.save()
        return redirect('dbs_list')

    return render(request, template_name, {'form': form,
                                           'username': username,
                                           'var8': 'active',
                                           'highlight1': 'active',
                                           'dbs': dbs,
                                           's': s,
                                           'zones': zones,
                                           '_select': _select,
                                           })


@login_required
@permission_required('dbs_mysql.delete_databases', raise_exception=True)
def database_del(request):
    pk = request.GET['id']
    dbs = get_object_or_404(Databases, pk=int(pk))
    dbs.delete()
    return HttpResponse('delete success')


@login_required
@permission_required('dbs_mysql.view_databases', raise_exception=True)
def database_detail(request, pk, template_name='databases/database_detail.html'):
    try:
        db = Databases.objects.get(pk=pk)
        # data = {
        #     'ip_address': dbs.ip_address,
        #     'password': dbs.root_password,
        # }
        # process = MySQLUserProcess(**data)
        # user_dict_object = process.get_mysql_users()
        # print user_dict_object
        # for item in user_dict_object:
        #     if DBAccounts.objects.filter(hosts=item['Host'], username=item['User']):
        #         pass
        #     else:
        #         dba = DBAccounts(databases_id=pk, hosts=item['Host'], username=item['User'])
        #         dba.save()
        # dba_object = DBAccounts.objects.filter(databases_id=pk)
    except Databases.DoesNotExist:
        raise Http404
    return render(request, template_name, {'db': db,
                                           'var8': 'active',
                                           'username': request.session['username'],
                                           'highlight1': 'active',
                                           # 'dba_object': dba_object,
                                           })


# @login_required
# @permission_required('Databases.view_databases', raise_exception=True)
# def database_detail(request, pk, template_name='databases/database_detail.html'):
#     try:
#         dbs = MySQL.objects.get(pk=pk)
#         # print dbs.ip_address
#         # print dbs.root_password
#         data = {
#             'ip_address': dbs.ip_address,
#             'password': dbs.root_password,
#         }
#         process = MySQLUserProcess(**data)
#         user_dict_object = process.get_mysql_users()
#         print user_dict_object
#         for item in user_dict_object:
#             # print "account: ", item['User'], "hosts: ", item['Host']
#             # print DBAccounts.objects.filter(hosts=item['Host'], username=item['User'])
#             if DBAccounts.objects.filter(hosts=item['Host'], username=item['User']):
#                 pass
#                 # print "here"
#                 # return HttpResponse('object already exists.')
#             else:
#                 # print "else here"
#                 dba = DBAccounts(databases_id=pk, hosts=item['Host'], username=item['User'])
#                 dba.save()
#         dba_object = DBAccounts.objects.filter(databases_id=pk)
#     except MySQL.DoesNotExist:
#         raise Http404
#     return render(request, template_name, {'dbs': dbs,
#                                            'var8': 'active',
#                                            'username': request.session['username'],
#                                            'highlight1': 'active',
#                                            'dba_object': dba_object,
#                                            })


# @login_required
# @permission_required('Databases.view_dba', raise_exception=True)
# def db_account_list(request, template_name='databases/dba_list.html'):
#     username = request.session['username']
#     db_accounts = DBAccounts.objects.all()
#     highlight2 = 'active'
#     var8 = 'active'
#     return render(request, template_name, locals())
#
#
# @login_required
# @permission_required('Databases.add_dba', raise_exception=True)
# def db_account_add(request, template_name='databases/dba_add.html'):
#     form = DBAForm(request.POST or None)
#     username = request.session['username']
#     dbs = DBAccounts.objects.all()
#     if form.is_valid():
#         print form
#         form.save()
#         return redirect('dba_list')
#
#     return render(request, template_name, {'form': form,
#                                            'username': username,
#                                            'var8': 'active',
#                                            'highlight2': 'active',
#                                            'dbs': dbs,
#                                            })
#
#
# @login_required
# @permission_required('Databases.change_dba', raise_exception=True)
# def db_account_edit(request, pk, template_name='databases/dba_add.html'):
#     username = request.session['username']
#     db_accounts = get_object_or_404(DBAccounts, pk=pk)
#     select = db_accounts.databases
#     dbs = DBAccounts.objects.all()
#     form = DBAForm(request.POST or None, instance=db_accounts)
#     if form.is_valid():
#         form.save()
#         return redirect('dba_list')
#
#     return render(request, template_name, {'form': form,
#                                            'username': username,
#                                            'var8': 'active',
#                                            'highlight2': 'active',
#                                            'db_accounts': db_accounts,
#                                            'select': select,
#                                            'dbs': dbs,
#                                            })
#
#
# @login_required
# @permission_required('Databases.delete_dba', raise_exception=True)
# def db_account_del(request):
#     pk = request.GET['id']
#     db_accounts = get_object_or_404(DBAccounts, pk=int(pk))
#     db_accounts.delete()
#     return HttpResponse('delete success')
#
#
# @login_required
# @permission_required('Databases.view_dba', raise_exception=True)
# def db_account_detail(request, pk, template_name='databases/dba_detail.html'):
#     try:
#         db_accounts = DBAccounts.objects.get(pk=pk)
#     except DBAccounts.DoesNotExist:
#         raise Http404
#     return render(request, template_name, {'db_accounts': db_accounts,
#                                            'var8': 'active',
#                                            'username': request.session['username'],
#                                            'highlight2': 'active',
#                                            })
