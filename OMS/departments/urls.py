from django.conf.urls import patterns, url
from s import views


urlpatterns = patterns('',
                       # dep
                       url(r'^_add/', views._add, name='_add'),
                       url(r'^_del/', views._del, name='_del'),
                       url(r'^_edit/(?P<pk>\d+)$', views._edit, name='_edit'),
                       url(r'^_list/', views._list, name='_list'),
                       url(r'^_detail/(?P<pk>\d+)$', views._detail, name='_detail'),
#                       url(r'^_search/$', views._search, name='_search'),
                       )
