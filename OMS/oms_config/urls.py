# from django.conf.urls import url
from django.conf.urls import patterns, url
from oms_config import zone_views, info_views, upload_views, path_views, produce_views
from oms_config import domain_views


urlpatterns = patterns('',
                       # zone_info
                       url(r'^produce_add', produce_views.produce_add, name='produce_add'),
                       url(r'^produce_edit/(?P<pk>\d+)$', produce_views.produce_edit, name='produce_edit'),
                       url(r'^produce_del/', produce_views.produce_del, name='produce_del'),
                       url(r'^produce_list/', produce_views.produce_list, name='produce_list'),
                       url(r'^produce_detail/(?P<pk>\d+)$', produce_views.produce_detail, name='produce_detail'),
                       # file_upload
                       url(r'^upload_list/', upload_views.upload_file_list, name='upload_list'),
                       url(r'^upload_file/', upload_views.file_upload, name='upload_file'),
                       url(r'^upload_del/', upload_views.upload_del, name='upload_del'),
                       url(r'^multi_file_upload/', upload_views.multi_file_upload, name='multi_file_upload'),
                       url(r'^upload_action/', upload_views.upload_action, name='upload_action'),
                       url(r'^show_files/(?P<pk>\d+)$', upload_views.show_files, name='show_files'),
                       # game_zone
                       url(r'^game_zone_list/$', zone_views.game_zone_list, name='game_zone_list'),
                       url(r'^game_zone_add/$', zone_views.game_zone_add, name='game_zone_add'),
                       url(r'^game_zone_edit/(?P<pk>\d+)$', zone_views.game_zone_edit, name='game_zone_edit'),
                       url(r'^game_zone_del/', zone_views.game_zone_del, name='game_zone_del'),
                       url(r'^game_zone_detail/(?P<pk>\d+)$', zone_views.game_zone_detail, name='game_zone_detail'),
                       # info
                       url(r'^info_add', info_views.info_add, name='info_add'),
                       url(r'^info_edit/(?P<pk>\d+)$', info_views.info_edit, name='info_edit'),
                       url(r'^info_del/', info_views.info_del, name='info_del'),
                       url(r'^info_list/', info_views.info_list, name='info_list'),
                       url(r'^info_detail/(?P<pk>\d+)$', info_views.info_detail, name='info_detail'),
                       url(r'^game_zone_copy/', info_views.game_zone_copy, name='game_zone_copy'),
                       url(r'^get_zones/(?P<pk>\d+)$', info_views.get_zones, name='get_zones'),
                       # domain
                       url(r'^domain_add/', domain_views.domain_add, name='domain_add'),
                       url(r'^domain_del/', domain_views.domain_del, name='domain_del'),
                       url(r'^domain_edit/(?P<pk>\d+)$', domain_views.domain_edit, name='domain_edit'),
                       url(r'^domain_list/', domain_views.domain_list, name='domain_list'),
                       url(r'^domain_detail/(?P<pk>\d+)$', domain_views.domain_detail, name='domain_detail'),
                       # path
                       url(r'^path_add/', path_views.path_add, name='path_add'),
                       url(r'^path_del/', path_views.path_del, name='path_del'),
                       url(r'^path_edit/(?P<pk>\d+)$', path_views.path_edit, name='path_edit'),
                       url(r'^path_list/', path_views.path_list, name='path_list'),
                       url(r'^path_detail/(?P<pk>\d+)', path_views.path_detail, name='path_detail'),
                       )
