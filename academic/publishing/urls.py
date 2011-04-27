from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from academic.views import PlainTextDetailView
from academic.views import PlainTextListView

from academic.publishing.models import *
from academic.publishing.views import PublicationListView

urlpatterns = patterns(
    '',

    url(r'^v/(?P<slug>[-\w]+)\.bib$',
        cache_page(PlainTextDetailView.as_view(
                model=Publication,
                template_name='academic/publication_detail.bib')),
        name='academic_publishing_publication_detail_bibtex'),

    url(r'^v/(?P<slug>[-\w]+)$',
        cache_page(DetailView.as_view(
                model=Publication,
                template_name='academic/publication_detail.html')),
        name='academic_publishing_publication_detail'),

    url(r'^bibtex$',
        cache_page(PlainTextListView.as_view(
                model=Publication,
                template_name='academic/publication_list.bib')),
        name='academic_publishing_publication_list_bibtex'),
    
    url(r'^$',
        cache_page(PublicationListView.as_view()),
        name='academic_publishing_publication_list'),
    )
