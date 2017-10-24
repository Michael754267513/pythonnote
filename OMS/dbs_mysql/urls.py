from django.conf.urls import patterns, url
from dbs_mysql import views


urlpatterns = patterns('',
                       # dbs
                       url(r'^database_add/', views.database_add, name='dbs_add'),
                       url(r'^database_del/', views.database_del, name='dbs_del'),
                       url(r'^database_edit/(?P<pk>\d+)$', views.database_edit, name='dbs_edit'),
                       url(r'^database_list/', views.database_list, name='dbs_list'),
                       url(r'^database_detail/(?P<pk>\d+)$', views.database_detail, name='dbs_detail'),
                       # attributes
                       # url(r'^dba_add/', views.dba_add, name='dba_add'),
                       # url(r'^dba_del/', views.dba_del, name='dba_del'),
                       # url(r'^dba_edit/(?P<pk>\d+)$', views.dba_edit, name='dba_edit'),
                       # url(r'^dba_list/', views.dba_list, name='dba_list'),
                       # url(r'^dba_detail/(?P<pk>\d+)', views.dba_detail, name='dba_detail'),
                       )
