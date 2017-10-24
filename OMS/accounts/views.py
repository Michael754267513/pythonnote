# --*-- coding:utf-8 --*--

from django.shortcuts import render, redirect, get_object_or_404, Http404
from forms import LoginUserForm, UserForm, EditUserForm, GroupForm, SetPasswordForm
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from accounts.models import User


# Create your views here.


def login(request, template_name='accounts/login.html'):
    if request.method == 'GET':
        form = LoginUserForm()
        return render(request, template_name, {'form': form})
    else:
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                if user.is_staff:
                    auth.login(request, user)
                    request.session['id'] = user.id
                    request.session['username'] = user.username
                    return redirect('dashboard')
                else:
                    return HttpResponse("用户非staff用户，禁止登陆后台")
            else:
                return render(request,
                              template_name, {'from': form, 'password_is_wrong': True}
                              )
        else:
            return render(request, template_name, {'form': form})


@login_required
def user_list(request, template_name='accounts/user_list.html'):
    username = request.session['username']
    user = get_object_or_404(User, username=username)
    has_perms = user.has_perm('user.add_user')
    data = {}
    var2 = 'active'
    users = User.objects.all()
    data['object_list'] = users
    data['var2'] = var2
    data['highlight2'] = 'active'
    data['username'] = username
    data['has_perms'] = has_perms

    return render(request, template_name, data)


@login_required
def user_add(request, template_name='accounts/user_add.html'):
    username = request.session['username']
    permission = 'auth.add_user'
    if current_user_permissions(username, permission):
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                username, password = form.cleaned_data['username'], form.cleaned_data['password1']
                new_user = User.objects.create_user(username=username, password=password)
                new_user.is_active = True      # if you want to set active
                new_user.save()
                return redirect('user_list')
        else:
            form = UserForm()
        return render(request, template_name, {'form': form, 'username': username, 'var2': 'active'})
    else:
        return HttpResponse("权限不够")


@login_required
def user_edit(request, pk, template_name='accounts/user_edit.html'):
    user = get_object_or_404(User, pk=pk)
    uid = pk
    print uid
    username = request.session['username']
    permission = 'auth.change_user'
    if current_user_permissions(username, permission):
        form = EditUserForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        return render(request, template_name, {'form': form, 'username': username, 'uid': pk})
    else:
        return HttpResponse("权限不够")


def user_detail(request, pk, template_name='accounts/user_detail.html'):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404
    return render(request, template_name, {'user': user,
                                           'var2': 'active',
                                           'highlight2': 'active',
                                           'username': request.session['username']})

# @login_required
# def user_delete(request, pk, template_name='Accounts/user_confirm_delete.html'):
#     user = get_object_or_404(User, pk=pk)
#     username = request.session['username']
#     permission = 'auth.delete_user'
#     if current_user_permissions(username, permission):
#         if request.method == 'POST':
#             user.delete()
#             return redirect('user_list')
#         return render(request, template_name, {'object': user, 'username': username})
#     else:
#         return HttpResponse("权限不够")

@login_required
@permission_required('User.delete_user', raise_exception=True)
def user_delete(request):
    pk = int(request.GET['id'])
    print pk
    user = get_object_or_404(User, pk=pk)
    user.delete()

    return HttpResponse('delete success')


@login_required
def group_list(request, template_name='accounts/group_list.html'):
    username = request.session['username']
    data = {}
    var2 = 'active'
    data['username'] = username
    data['var2'] = var2
    data['highlight1'] = 'active'
    groups = Group.objects.all()
    data['object_list'] = groups

    return render(request, template_name, data)


@login_required
def group_add(request, template_name='accounts/group_add.html'):
    permission_list = Permission.objects.all()
    username = request.session['username']
    permission = 'auth.add_group'
    if current_user_permissions(username, permission):
        if request.method == 'POST':
            form = GroupForm(request.POST, request.FILES)
            if form.is_valid():
                print form
                group = form.save(commit=False)
                group.save()
            return redirect('group_list')
        else:
            form = GroupForm()
        return render(request, template_name, {'form': form,
                                               'username': username,
                                               'var2': 'active',
                                               'highlight1': 'active',
                                               'permission_list': permission_list})
    else:
        return HttpResponse("权限不够")


@login_required
def group_edit(request, pk, template_name='accounts/group_add.html'):
    permission_list = Permission.objects.all()
    username = request.session['username']
    permission = 'auth.change_group'
    if current_user_permissions(username, permission):
        group = get_object_or_404(Group, pk=pk)
        # for item in group.permissions.all():
        #     print item
        form = GroupForm(instance=group)
        if request.method == 'POST':
            form = GroupForm(request.POST, request.FILES, instance=group)
            if form.is_valid():
                form.save()
                return redirect('group_list')
        return render(request, template_name, {'form': form,
                                               'username': username,
                                               'group': group,
                                               'var2': 'active',
                                               'highlight1': 'active',
                                               'permission_list': permission_list})
    else:
        return HttpResponse('权限不够')


# @login_required
# def group_delete(request):
#     if request.method == 'POST':
#         pk = int(request.POST['id'])
#         username = request.session['username']
#         permission = 'auth.delete_group'
#         if current_user_permissions(username, permission):
#             group = get_object_or_404(Group, pk=pk)
#             print group
#             group.is_active = False
#             group.delete()
#             # return redirect('group_list')
#             return HttpResponse('success.')
#         else:
#             return HttpResponse('权限不够')
#         # return render(request, template_name, {'group': group, 'username': username})


@login_required
@permission_required('Group.delete_group', raise_exception=True)
def group_delete(request):
    pk = int(request.GET['id'])
    print pk
    group = get_object_or_404(Group, pk=pk)
    group.delete()
    return HttpResponse('delete success')


def group_detail(request, pk, template_name='accounts/group_detail.html'):
    try:
        group = Group.objects.get(pk=pk)
        # print group.permissions
    except Group.DoesNotExist:
        raise Http404
    return render(request, template_name, {'group': group,
                                           'var2': 'active',
                                           'highlight1': 'active',
                                           'username': request.session['username']})


@login_required
def permissions_list(request, template_name='Accounts/permissions_list.html'):
    username = request.session['username']
    data = {}
    permissions_page = 'current'
    data['username'] = username
    data['permissions_page'] = permissions_page
    # if User.objects.get(username=username).is_superuser:
    permissions = Permission.objects.all()
    # print permissions
    data['permission_list'] = permissions
    # else:
    #     return HttpResponse("你没有权限查看权限信息")
    return render(request, template_name, data)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('user_login')


def current_user_permissions(username, permission):
    current_user = get_object_or_404(User, username=username)
    if current_user.has_perm(permission):
        return True
    else:
        return False


@login_required
def password_reset(request, pk, template_name='Accounts/password_reset.html'):
    if request.method == 'GET':
        form = SetPasswordForm()
        return render(request, template_name, {'form': form, 'username': request.session['username']})
    else:
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            username = User.objects.get(pk=pk).username
            old_password = form.cleaned_data['old_password']
            user = auth.authenticate(username=username, password=old_password)
            if user is not None:
                # print "Here is OK"
                # if user.is_active:
                new_password = form.cleaned_data['verify_password']
                user.set_password(new_password)
                user.save()
                # messages.success(request, 'Password has been reset.')
                return redirect('user_list')
            else:
                # print "here is failed"
                return render(request, template_name, {'form': form, 'old_password_is_wrong': True,
                                                       'username': request.session['username']})
        else:
            return render(request, template_name, {'form': form, 'username': request.session['username']})


@login_required
def user_summary(request, template_name='accounts/user_group_index.html'):
    var2 = 'active'
    user_number = User.objects.all().count()
    group_number = Group.objects.all().count()
    superusers = User.objects.filter(is_superuser=True).count()

    return render(request, template_name, {'user_number': user_number,
                                           'group_number': group_number,
                                           'superusers': superusers,
                                           'var2': var2,
                                           'username': request.session['username']})

