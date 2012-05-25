"""
Here are the various URL's for the module. Tree.io does not use namespaces, but have the convention
to put the name of the module in front of the name. That's "achievements_" for this module.
"""
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('achievements.views',
        url(r'^(\.(?P<response_format>\w+))?$', 'index', name='achievements'),
        url(r'^user/(?P<user_id>\d+)/(\.(?P<response_format>\w+))?/?$', 'user', name='achievements_user_view'),
        url(r'^add/(\.(?P<response_format>\w+))?/?$', 'achievement_add', name='achievements_achievement_add'),
        url(r'^edit/(?P<achievement_id>\d+)/(\.(?P<response_format>\w+))?/?$', 'achievement_edit',
            name='achievements_achievement_edit'),
        url(r'^detail/(?P<achievement_id>\d+)/(\.(?P<response_format>\w+))?/?$', 'achievement_detail',
            name='achievements_achievement_detail'),
        url(r'^delete/(?P<achievement_id>\d+)/(\.(?P<response_format>\w+))?/?$', 'achievement_delete',
            name='achievements_achievement_delete'),

        url(r'^prototypes/(\.(?P<response_format>\w+))?/?$', 'prototypes', name='achievements_prototypes'),
        url(r'^prototype/add/(\.(?P<response_format>\w+))?/?$', 'prototype_add', name='achievements_prototype_add'),
        url(r'^prototype/edit/(?P<prototype_id>\d+)/(\.(?P<response_format>\w+))?/?$', 'prototype_edit',
            name='achievements_prototype_edit'),
        url(r'^prototype/detail/(?P<prototype_id>\d+)/(\.(?P<response_format>\w+))?/?$', 'prototype_detail',
            name='achievements_prototype_detail'),
        url(r'^prototype/delete/(?P<prototype_id>\d+)/(\.(?P<response_format>\w+))?/?$', 'prototype_delete',
            name='achievements_prototype_delete'),
)
