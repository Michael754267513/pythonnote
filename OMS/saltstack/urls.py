from django.conf.urls import patterns, url
from saltstack import views
from saltstack import release_views
from saltstack import p2p_scp_views
from saltstack import push_file_views
from saltstack import services_opreate_views
from saltstack import execute_cmd_views
from saltstack import crontab_views
from saltstack import all_update_views
from saltstack import system_user_views
from saltstack import change_pass_views
from saltstack import yum_install_views
from saltstack import code_backup_views
from saltstack import code_rollback_views
from saltstack import sync_config_views
from saltstack import merge_server_views
from saltstack import deploy_wizard_views


urlpatterns = patterns('',
                       # key manager
                       url(r'^salt_key_manager', views.salt_key_manager, name='salt_key_manager'),
                       url(r'^salt_key_accept/minion=(?P<minion>[\w\-]+)$', views.salt_key_accept,
                           name='salt_key_accept'),
                       url(r'^salt_key_delete/minion=(?P<minion>[\w\-]+)$', views.salt_key_delete,
                           name='salt_key_delete'),
                       url(r'^get_servers_info/minion=(?P<minion>[\w\-]+)$', views.get_servers_info,
                           name='get_servers_info'),
                       url(r'^cp_get_agent_dir/minion=(?P<minion>[\w\-]+)$', views.push_agent_scripts,
                           name='push_agent_scripts'),
                       url(r'^sync_grains/minion=(?P<minion>[\w\-]+)$', views.sync_grains, name='sync_grains'),

                       # code release
                       url(r'^code_release_list', release_views.code_release_list, name='code_release_list'),
                       url(r'^code_release/', release_views.code_release, name='code_release'),
                       url(r'^code_release_detail/(?P<pk>\d+)$', release_views.code_release_detail,
                           name='code_release_detail'),
                       url(r'^code_release_history_del/', release_views.code_release_history_del,
                           name='code_release_history_del'),

                       # code backup

                       url(r'^code_backup_list', code_backup_views.code_backup_list,
                           name='code_backup_list'),
                       url(r'^code_backup_process/', code_backup_views.code_backup_process,
                           name='code_backup_process'),
                       url(r'^code_backup_detail/(?P<pk>\d+)$', code_backup_views.code_backup_detail,
                           name='code_backup_detail'),
                       url(r'^code_backup_record_del/', code_backup_views.code_backup_record_del,
                           name='code_backup_record_del'),

                       # code rollback

                       url(r'^code_rollback_list', code_rollback_views.code_rollback_list,
                           name='code_rollback_list'),
                       url(r'^code_rollback_process/', code_rollback_views.code_rollback_process,
                           name='code_rollback_process'),
                       url(r'^code_rollback_detail/(?P<pk>\d+)$', code_rollback_views.code_rollback_detail,
                           name='code_rollback_detail'),
                       url(r'^code_rollback_record_del/', code_rollback_views.code_rollback_record_del,
                           name='code_rollback_record_del'),

                       # file push
                       url(r'^file_push_list', push_file_views.push_list, name='file_push_list'),
                       url(r'^file_push_process', push_file_views.push_process, name='file_push_process'),
                       url(r'^file_push_detail/(?P<pk>\d+)$', push_file_views.push_detail, name='file_push_detail'),
                       url(r'^file_push_history_del/', push_file_views.push_history_del, name='file_push_history_del'),

                       # services operate
                       url(r'^services_handle_list/', services_opreate_views.services_handle_list,
                           name='services_handle_list'),
                       url(r'^services_handle_process/', services_opreate_views.services_handle_process,
                           name='services_handle_process'),
                       url(r'^services_handle_del/', services_opreate_views.services_handle_del,
                           name='services_handle_del'),
                       url(r'^services_handle_detail/(?P<pk>\d+)$', services_opreate_views.services_handle_detail,
                           name='services_handle_detail'),

                       # execute command
                       url(r'^command_execute_list/', execute_cmd_views.command_execute_list,
                           name='command_execute_list'),
                       url(r'^command_execute_process/', execute_cmd_views.command_execute_process,
                           name='command_execute_process'),
                       url(r'^execute_history_del/', execute_cmd_views.execute_history_del,
                           name='execute_history_del'),
                       url(r'^command_execute_detail/(?P<pk>\d+)$', execute_cmd_views.execute_command_detail,
                           name='command_execute_detail'),

                       # cron jobs
                       url(r'^cron_list/', crontab_views.cron_list, name='cron_list'),
                       url(r'^cron_jobs/', crontab_views.cron_jobs, name='cron_jobs'),
                       url(r'^cron_detail/(?P<pk>\d+)$', crontab_views.cron_detail, name='cron_detail'),
                       url(r'^cron_history_del/', crontab_views.cron_history_del, name='cron_history_del'),
                       # url(r'^salt_introduction/', views.salt_introduction, name='salt_introduction'),
                       # url(r'^get_zones/(?P<pk>\d+)$', views.get_zones, name='get_zones'),
                       # url(r'^get_servers/(?P<pk>\d+)$', views.get_servers, name='get_servers'),
                       # url(r'^get_generate_file/(?P<pk>\d+)$', views.get_generate_file, name='get_generate_file'),
                       # url(r'^get_services/(?P<pk>\d+)$', views.get_services, name='get_services'),
                       # url(r'^get_servers_with_service/(?P<id_service>\d+)/(?P<id_>\d+)/(?P<id_game_zone>\d+)'
                       #     r'/$', views.get_servers_with_service, name='get_servers_with_service'),

                       # all zone update code
                       url(r'^all_zone_update_process/', all_update_views.all_zone_update_process,
                           name='all_zone_update_process'),
                       url(r'^all_zone_update_list/', all_update_views.all_zone_update_list,
                           name='all_zone_update_list'),
                       url(r'^all_zone_update_detail/(?P<pk>\d+)$', all_update_views.all_zone_update_detail,
                           name='all_zone_update_detail'),
                       url(r'all_zone_update_del/', all_update_views.all_zone_update_del,
                           name='all_zone_update_del'),

                       # sys user manager
                       url(r'system_user_list/', system_user_views.system_user_list, name='system_user_list'),
                       url(r'system_user_add/', system_user_views.system_user_add, name='system_user_add'),
                       url(r'system_user_del', system_user_views.system_user_del, name='system_user_del'),
                       url(r'system_user_operation_history_del/', system_user_views.system_user_operation_history_del,
                           name='system_user_operation_history_del'),
                       url(r'system_user_operate_detail/(?P<pk>\d+)$', system_user_views.system_user_operate_detail,
                           name='system_user_operate_detail'),

                       # change sys user password
                       url(r'change_password_record/', change_pass_views.change_password_record,
                           name='change_password_record'),
                       url(r'change_sys_password/', change_pass_views.change_sys_password,
                           name='change_sys_password'),
                       url(r'change_password_detail/(?P<pk>\d+)$', change_pass_views.change_password_detail,
                           name='change_password_detail'),
                       url(r'change_password_record_del/', change_pass_views.change_password_record_del,
                           name='change_password_record_del'),
                       # p2p scp
                       url(r'p2p_scp_process/', p2p_scp_views.p2p_scp_process, name='p2p_scp_process'),
                       url(r'unix2dos_tools/', push_file_views.unix2dos, name='unix2dos'),

                       # yum install package
                       url(r'yum_install_soft_record/', yum_install_views.yum_install_soft_record,
                           name='yum_install_soft_record'),
                       url(r'yum_install_soft_process/', yum_install_views.yum_install_soft_process,
                           name='yum_install_soft_process'),
                       url(r'yum_install_record_del/', yum_install_views.yum_install_record_del,
                           name='yum_install_record_del'),
                       url(r'yum_install_soft_detail/(?P<pk>\d+)$', yum_install_views.yum_install_soft_detail,
                           name='yum_install_soft_detail'),

                       # sync config
                       url(r'sync_config_list/', sync_config_views.sync_config_list,
                           name='sync_config_list'),
                       url(r'sync_config_process/', sync_config_views.sync_config_process,
                           name='sync_config_process'),
                       url(r'sync_config_record_del/', sync_config_views.sync_config_record_del,
                           name='sync_config_record_del'),
                       url(r'sync_config_detail/(?P<pk>\d+)$', sync_config_views.sync_config_detail,
                           name='sync_config_detail'),

                       # merge server
                       url(r'merge_server_list/', merge_server_views.merge_server_list,
                           name='merge_server_list'),
                       url(r'merge_server_process/', merge_server_views.merge_server_process,
                           name='merge_server_process'),
                       url(r'merge_server_record_del/', merge_server_views.merge_server_record_del,
                           name='merge_server_record_del'),
                       url(r'merge_server_detail/(?P<pk>\d+)$', merge_server_views.merge_server_detail,
                           name='merge_server_detail'),

                       url(r'^deploy_game_wizard_list/', deploy_wizard_views.deploy_game_wizard_list,
                           name='deploy_game_wizard_list'),
                       url(r'^deploy_game_wizard/', deploy_wizard_views.deploy_game_wizard, name='deploy_game_wizard'),
                       url(r'^deploy_game_wizard_del/', deploy_wizard_views.deploy_game_wizard_del,
                           name='deploy_game_wizard_del'),
                       url(r'^deploy_game_wizard_detail/(?P<pk>\d+)$', deploy_wizard_views.deploy_game_wizard_detail,
                           name='deploy_game_wizard_detail'),

                       )
