# encoding: utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import loader, Context
from django.core.urlresolvers import reverse
from test import *
from models import *

from django.db import connection


def hostadd(request):
    if request.method == "GET":

        return render_to_response("host/hostadd.html")
    if request.method == "POST":
        ip_list = HostList.objects.all
        VarsList = request.POST
        HostList.objects.create(ip=VarsList["ip"],
                                ug=UserGroup.objects.get(id=VarsList["ug_id"]),
                                hg=HostGroup.objects.get(id=VarsList["hg_id"]))
        return render_to_response("host/hostdel.html",{"iplist":ip_list})


def hostlist(request):
    if request.method == "GET":
        ip = request.GET.get("ip" )
        if ip:
            ip_list = HostList.objects.filter(ip__contains=ip)
        else:
            ip_list = HostList.objects.all

        return render_to_response("host/hostlist.html", {"iplist":ip_list, })


def index(request):
    #t = loader.get_template("html.html")
    #c = Context({"name": "michael"})
    #c = Context({})
    #text = t.render(c)
    return HttpResponse("Michael")


def useradd(request):
    print request.GET.get("name")
    print type(UserType.objects)
    #UserType.objects.create(Name=request.GET.get("name"))
    #UserType.objects.get(Name=request.GET.get("name")).delete()
    '''obj = UserType.objects.get(Name=request.GET.get("name"))
    obj.Name = "michael"
    obj.save()'''#改
    #cursor = connection.cursor()
    #cursor.execute('''SELECT Name FROM web_UserType WHERE Name = %s''', ['michael'])
    #row = cursor.fetchone()
    #name = UserType.objects.get(Name=request.GET.get("name")).Name

    return HttpResponse(name)


def UserList(request):
    user_list = UserType.objects.all()
    return  render_to_response("user/userlists.html",{"userlist":user_list})

def UserName(request):
    user_list = UserType.objects.all()
    return  render_to_response("user/username.html",{"userlist":user_list})

# '''调用一个方法'''
def def_def(request):
    t = loader.get_template("index.html")
    c = Context({"name": index1()})
    text = t.render(c)
    return HttpResponse(text)

# '''调用一个数组'''
def sz(request):
    t = loader.get_template("index.html")
    c = Context({"computer": computer})
    text = t.render(c)
    return HttpResponse(text)


# '''调用一个字典'''
def directory_d(request):
    t = loader.get_template("index.html")
    c = Context({"dir": directory, "name": "michael"})
    text = t.render(c)
    return HttpResponse(text)
phone = phone("HuaWei", "3g")
name = phone.name
memory = phone.memory


# '''调用一个类'''
def class_c(request):
    t = loader.get_template("index.html")
    c = Context({"phone": name, "memory": memory})
    text = t.render(c)
    return HttpResponse(text)


# '''带参数的uri'''
def url(request):
    t = loader.get_template("index.html")
    name = request.GET.get("name")
    #设置默认值
    age = request.GET.get("age",20)
    c = Context({"name": name, "age": age})
    text = t.render(c)
    return HttpResponse(text)


# '''带参数的uri,正则urls'''
def urlp(request,name,age):
    t = loader.get_template("index.html")
    c = Context({"name": name,"age":age})
    text = t.render(c)
    return HttpResponse(text)


def root_r(request):
    t = loader.get_template("index.html")
    c = Context({})
    text = t.render(c)
    return HttpResponse(text)
################################urls##################


# 301 重定向,携带参数重定向到urlp
def redirect_r(request, name1, age):
   return HttpResponse(reverse('urlp',args=(name1,age)))