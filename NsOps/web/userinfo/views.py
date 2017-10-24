# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpRequest
from django.template import loader, Context
from django.core.urlresolvers import reverse
# Create your views here


def index(request):

    return HttpResponse("userinfo")


def login(request):
    name = request.GET.get('name')
    passwd = request.GET.get('passwd')
    print name,passwd
    return HttpResponse("userinfo/login")