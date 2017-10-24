from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from assets.models import Assets
from django.contrib.auth.models import Group
from accounts.models import User
from s.models import

# Create your views here.


@login_required
def index(request, template_name='dashboard/index.html'):
    if request.session['id'] is not None:
        username = request.session['username']
        # print username
        var1 = 'active'

        on_line_number = Assets.objects.filter(is_online=True).count()
        unused_number = Assets.objects.filter(is_unused=True).count()
        server_list = '%s %s' % (on_line_number, unused_number)

        user_number = User.objects.all().count()
        group_number = Group.objects.all().count()
        _number = .objects.all().count()
        account_list = '%s %s %s' % (group_number, user_number, _number)
        unused_servers = Assets.objects.filter(is_unused=True)

        return render(request, template_name, {'username': username,
                                               'var1': var1,
                                               'server_list': server_list,
                                               'account_list': account_list,
                                               'unused_servers': unused_servers,
                                               })
    else:
        return redirect('user_login')
