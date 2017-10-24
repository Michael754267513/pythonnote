from django.conf.urls import patterns, url
from dbs_redis import views


urlpatterns = patterns('',
                       # dbs
                       url(r'^redis_add/', views.dbs_redis_add, name='dbs_redis_add'),
                       url(r'^redis_del/', views.dbs_redis_del, name='dbs_redis_del'),
                       url(r'^redis_edit/(?P<pk>\d+)$', views.dbs_redis_edit, name='dbs_redis_edit'),
                       url(r'^redis_list/', views.dbs_redis_list, name='dbs_redis_list'),
                       url(r'^redis_detail/(?P<pk>\d+)$', views.dbs_redis_detail, name='dbs_redis_detail'),
                       )
