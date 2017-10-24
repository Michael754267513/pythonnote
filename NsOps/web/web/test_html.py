from django.http import HttpResponse
from django.template import loader, Context
from test import *


def html(request):
    t = loader.get_template("html.html")
    c = Context({"dir": directory})
    text = t.render(c)
    return HttpResponse(text)
