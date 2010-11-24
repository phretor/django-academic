from django.conf.urls.defaults import *
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list, object_detail

urlpatterns = patterns(
    '',
    
    url(r'^publishing/', include('academic.publishing.urls')),
    url(r'^people/', include('academic.people.urls')),
    url(r'^organizations/', include('academic.organizations.urls')),
    url(r'^projects/', include('academic.projects.urls')),
    url(r'^content/', include('academic.content.urls')),
)
