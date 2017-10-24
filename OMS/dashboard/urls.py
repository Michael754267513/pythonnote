from django.conf.urls import *
from dashboard import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='dashboard'),
                       )

