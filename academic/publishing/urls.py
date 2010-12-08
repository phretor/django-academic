from django.conf.urls.defaults import *
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list, object_detail

from academic.publishing.models import *

urlpatterns = patterns(
    '',

    url(r'^v/(?P<slug>[-\w]+)\.bib$',
        cache_page(object_detail, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/publication_detail.bib',
         'mimetype': 'text/plain',
         'queryset': Publication.objects.all() },
        name='academic_publishing_publication_detail_bibtex'),

    url(r'^v/(?P<slug>[-\w]+)$',
        cache_page(object_detail, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/publication_detail.html',
         'queryset': Publication.objects.all() },
        name='academic_publishing_publication_detail'),

    url(r'^bibtex$',
        cache_page(object_list, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/publication_list.bib',
         'mimetype': 'text/plain',
         'queryset': Publication.objects.all() },
        name='academic_publishing_publication_list_bibtex'),

    url(r'^$',
        cache_page(object_list, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/publication_list.html',
         'queryset': Publication.objects.all() },
        name='academic_publishing_publication_list'),

)
