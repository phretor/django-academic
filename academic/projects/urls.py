from django.conf.urls.defaults import *
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list, object_detail

from academic.projects.models import *

urlpatterns = patterns(
    '',

    url(r'^topics/(?P<slug>[-\w]+)/$',
        cache_page(object_detail, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/topic_detail.html',
         'queryset': Topic.objects.all() },
        name='academic_projects_topic_detail'),

    url(r'^topics/$',
        cache_page(object_list, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/topic_list.html',
         'queryset': Topic.objects.all() },
        name='academic_projects_topic_list'),
        
    url(r'^projects/(?P<slug>[-\w]+)/$',
        cache_page(object_detail, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/project_detail.html',
         'queryset': Project.objects.all() },
        name='academic_projects_project_detail'),

    url(r'^projects/$',
        cache_page(object_list, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/project_list.html',
         'queryset': Project.objects.all() },
        name='academic_projects_project_list'),
)
