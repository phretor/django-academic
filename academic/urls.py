from django.conf.urls.defaults import *
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list, object_detail

from academic.models import *
from academic.views import *

urlpatterns = patterns(
    '',

    url(r'^sponsors/$',
        cache_page(object_list, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/sponsor_list.html',
         'queryset': Sponsor.objects.all() },
        name='academic_sponsor_list'),

    url(r'^people/$',
        cache_page(object_list, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/person_list.html',
         'queryset': Person.objects.all() },
        name='academic_person_list'),

    url(r'^topics/(?P<object_id>\d+)/$',
        cache_page(object_detail, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/topic_detail.html',
         'queryset': Topic.objects.all() },
        name='academic_topic_detail'),

    url(r'^topics/$',
        cache_page(object_list, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/topic_list.html',
         'queryset': Topic.objects.all() },
        name='academic_topic_list'),
        
    url(r'^projects/$',
        cache_page(object_list, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/project_list.html',
         'queryset': Project.objects.all() },
        name='academic_project_list'),

    url(r'^projects/(?P<object_id>\d+)/$',
        cache_page(project_detail, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/project_detail.html',
         'queryset': Project.objects.all() },
        name='academic_project_detail'),

    url(r'^publications/$',
        cache_page(object_list, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/publication_list.html',
         'queryset': Publication.objects.all() },
        name='academic_publication_list'),
)
