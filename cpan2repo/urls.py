from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'webui.views.index', name='index'),
                       url(r'^add_build_conf/$', 'webui.views.add_build_conf', name='add_build_conf'),
                       url(r'^autobuild_on_off/(?P<build_conf_id>\d+)$', 'webui.views.autobuild_on_off',
                           name='autobuild_on_off'),
                       url(r'^view_log/(?P<build_conf_id>\d+)$', 'webui.views.view_log', name='view_log'),
                       url(r'^edit_build_conf/(?P<build_conf_id>\d+)$', 'webui.views.edit_build_conf',
                           name='edit_build_conf'),
                       url(r'^remove_build_conf/(?P<build_conf_id>\d+)$', 'webui.views.remove_build_conf',
                           name='remove_build_conf'),
                       url(r'^rebuild_package/(?P<build_conf_id>\d+)$', 'webui.views.rebuild_package',
                           name='rebuild_package'),
                       url(r'^rebuild_all_packages/$', 'webui.views.rebuild_all_packages', name='rebuild_all_packages'),
                       url(r'^build_confs_list/$', 'webui.views.build_confs_list', name='build_confs_list'),

                       url(r'^branches_list/$', 'webui.views.branches_list', name='branches_list'),
                       url(r'^add_branch/$', 'webui.views.add_branch', name='add_branch'),
                       url(r'^edit_branch/(?P<branch_id>\d+)$', 'webui.views.edit_branch', name='edit_branch'),
                       url(r'^remove_branch/(?P<branch_id>\d+)$', 'webui.views.remove_branch', name='remove_branch'),

                       url(r'^branches_list/$', 'webui.views.branches_list', name='branches_list'),
                       url(r'^add_branch/$', 'webui.views.add_branch', name='add_branch'),
                       url(r'^edit_branch/(?P<branch_id>\d+)$', 'webui.views.edit_branch', name='edit_branch'),
                       url(r'^remove_branch/(?P<branch_id>\d+)$', 'webui.views.remove_branch', name='remove_branch'),

                       url(r'^mapping_list/$', 'webui.views.mapping_list', name='mapping_list'),
                       url(r'^add_mapping/$', 'webui.views.add_mapping', name='add_mapping'),
                       url(r'^edit_mapping/(?P<mapping_id>\d+)$', 'webui.views.edit_mapping', name='edit_mapping'),
                       url(r'^remove_mapping/(?P<mapping_id>\d+)$', 'webui.views.remove_mapping',
                           name='remove_mapping'),
                       url(r'^rebuild_packages_by_branch/(?P<branch_id>\d+)$', 'webui.views.rebuild_packages_by_branch',
                           name='rebuild_packages_by_branch'),

                       url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},
                           name="login"),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'},
                           name="logout"),
                       url(r'^admin/', include(admin.site.urls)),
)
