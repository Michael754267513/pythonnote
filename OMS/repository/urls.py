# -*- coding:utf8 -*-

from django.conf.urls import patterns, url
from repository import views


urlpatterns = patterns('',
                       url(r'^repository_add/', views.repository_add, name='repository_add'),
                       url(r'^repository_del/', views.repository_del, name='repository_del'),
                       url(r'^repository_edit/(?P<pk>\d+)$', views.repository_edit, name='repository_edit'),
                       url(r'^repository_detail/(?P<pk>\d+)$', views.repository_detail, name='repository_detail'),
                       url(r'^repository_list/', views.repository_list, name='repository_list'),

                       # 仓库版本
                       url(r'^repo_version_add/', views.repo_version_add, name='repo_version_add'),
                       url(r'^repo_version_del/', views.repo_version_del, name='repo_version_del'),
                       url(r'^repo_version_detail/(?P<pk>\d+)$', views.repo_version_detail, name='repo_version_detail'),
                       url(r'^repo_version_list/', views.repo_version_list, name='repo_version_list'),

                       # local archive
                       url(r'^local_archive_process/', views.local_archive_process, name='local_archive_process'),

                       )
