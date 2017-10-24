# -*- coding=utf-8 -*-

from django.conf.urls import patterns, url
from assets import views


urlpatterns = patterns('',
                       # network
                       url(r'^network_add$', views.network_add, name='network_add'),
                       url(r'^network_del/', views.network_del, name='network_del'),
                       url(r'^network_edit/(?P<pk>\d+)$', views.network_edit, name='network_edit'),
                       url(r'^network_list/', views.network_list, name='network_list'),
                       # url(r'^network_detail/(?P<pk>\d+)', views.network_detail, name='network_detail'),
                       # assets
                       url(r'^assets_list/$', views.assets_list, name='assets_list'),
                       url(r'^assets_add/$', views.assets_add, name='assets_add'),
                       url(r'^assets_edit/(?P<pk>\d+)/$', views.assets_edit, name='assets_edit'),
                       url(r'^assets_del/', views.assets_delete, name='assets_del'),
                       url(r'^assets_detail/(?P<pk>\d+)/$', views.assets_detail, name='assets_detail'),
                       # hardware
                       url(r'^hardware_add/$', views.hardware_add, name='hardware_add'),
                       url(r'^hardware_list/$', views.hardware_list, name='hardware_list'),
                       url(r'^hardware_edit/(?P<pk>\d+)$', views.hardware_edit, name='hardware_edit'),
                       url(r'^hardware_del/', views.hardware_del, name='hardware_del'),
                       # url(r'^hardware_detail/(?P<pk>\d+)$', views.hardware_detail, name='hardware_detail'),
                       # services
                       url(r'service_list/', views.service_list, name='service_list'),
                       url(r'service_add/', views.service_add, name='service_add'),
                       url(r'service_edit/(?P<pk>\d+)$', views.service_edit, name='service_edit'),
                       url(r'service_del/', views.service_delete, name='service_del'),
                       # tags
                       url(r'tag_list/', views.tag_list, name='tag_list'),
                       url(r'tag_add/', views.tag_add, name='tag_add'),
                       url(r'tag_edit/(?P<pk>\d+)$', views.tag_edit, name='tag_edit'),
                       url(r'tag_del/', views.tag_delete, name='tag_del'),
                       # make on or off
                       url(r'make_server_online/server=(?P<server>[\w\-]+)$', views.make_server_online,
                           name='make_servers_online'),
                       url(r'servers_offline/server=(?P<server>[\w\-]+)$', views.make_server_offline,
                           name='servers_offline'),
                       url(r'delete_assets_and_networks_from_database/server=(?P<server>[\w\-]+)$',
                           views.delete_assets_and_networks_from_database,
                           name='delete_assets_and_networks_from_database'),
                       url(r'^get_servers/(?P<pk>\d+)$', views.get_servers, name='get_servers'),
                       )
