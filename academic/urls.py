from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    
    url(r'^publishing/', include('academic.publishing.urls')),
    url(r'^people/', include('academic.people.urls')),
    url(r'^organizations/', include('academic.organizations.urls')),
    url(r'^projects/', include('academic.projects.urls')),
    url(r'^content/', include('academic.content.urls')),
)
