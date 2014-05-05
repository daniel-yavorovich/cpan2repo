# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'webui.views.index', name='index'),

                       url(r'^add_build_conf/(.*)/$', 'webui.views.add_build_conf', name='add_build_conf'),
                       url(r'^add_build_conf/$', 'webui.views.add_build_conf', name='add_build_conf'),

                       url(r'^view_log/(?P<build_conf_id>\d+)$', 'webui.views.view_log', name='view_log'),
                       url(r'^edit_build_conf/(?P<build_conf_id>\d+)$', 'webui.views.edit_build_conf',
                           name='edit_build_conf'),

                       url(r'^add_branch/$', 'webui.views.add_branch', name='add_branch'),
                       url(r'^edit_branch/(?P<branch_id>\d+)$', 'webui.views.edit_branch', name='edit_branch'),

                       url(r'^add_mapping/$', 'webui.views.add_mapping', name='add_mapping'),
                       url(r'^edit_mapping/(?P<mapping_id>\d+)$', 'webui.views.edit_mapping', name='edit_mapping'),

                       url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},
                           name="login"),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'},
                           name="logout"),

                       url(r'^admin/', include(admin.site.urls)),
)

# API
urlpatterns += patterns('webui.views',
                        url(r'^api/build_confs/$', 'build_confs'),
                        url(r'^api/branches/$', 'branches'),
                        url(r'^api/mapping/$', 'mapping'),

                        url(r'^api/rebuild_package/(?P<build_conf_id>\d+)$', 'rebuild_package'),
                        url(r'^api/autobuild_on_off/(?P<build_conf_id>\d+)$', 'autobuild_on_off'),
                        url(r'^api/global_autobuild_on/$', 'global_autobuild_on'),
                        url(r'^api/global_autobuild_off/$', 'global_autobuild_off'),
                        url(r'^api/remove_build_conf/(?P<build_conf_id>\d+)$', 'remove_build_conf'),
                        url(r'^api/remove_branch/(?P<branch_id>\d+)$', 'remove_branch'),
                        url(r'^api/remove_mapping/(?P<mapping_id>\d+)$', 'remove_mapping'),
)