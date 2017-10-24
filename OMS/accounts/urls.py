from django.conf.urls import patterns, url
from accounts import views


urlpatterns = patterns('',
                       url(r'login/', views.login, name='user_login'),
                       url(r'logout/', views.logout, name='user_logout'),
                       url(r'user_list/', views.user_list, name='user_list'),
                       url(r'user_add/', views.user_add, name='user_add'),
                       url(r'user_edit/(?P<pk>\d+)$', views.user_edit, name='user_edit'),
                       url(r'user_detail/(?P<pk>\d+)$', views.user_detail, name='user_detail'),
                       url(r'user_delete/', views.user_delete, name='user_delete'),
                       url(r'group_add/', views.group_add, name='group_add'),
                       url(r'group_list/', views.group_list, name='group_list'),
                       url(r'group_edit/(?P<pk>\d+)$', views.group_edit, name='group_edit'),
                       url(r'group_detail/(?P<pk>\d+)$', views.group_detail, name='group_detail'),
                       url(r'group_delete/', views.group_delete, name='group_delete'),
                       url(r'permission_list/', views.permissions_list, name='permissions_list'),
                       url(r'password_reset/(?P<pk>\d+)$', views.password_reset, name='password_reset'),
                       url(r'user_summary/', views.user_summary, name='user_summary'),
                       )
