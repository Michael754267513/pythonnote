from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',

                       url(r'accounts/', include('accounts.urls')),
                       url(r'dashboard/', include('dashboard.urls')),
                       url(r's/', include('s.urls')),
                       url(r'oms_config/', include('oms_config.urls')),
                       url(r'dbs_mysql/', include('dbs_mysql.urls')),
                       url(r'dbs_redis/', include('dbs_redis.urls')),
                       url(r'repository/', include('repository.urls')),
                       url(r'assets/', include('assets.urls')),
                       url(r'saltstack/', include('saltstack.urls')),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),
                       )
