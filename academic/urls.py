from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    
    url(r'^publishing/', include('academic.apps.publishing.urls')),
    url(r'^people/', include('academic.apps.people.urls')),
    url(r'^organizations/', include('academic.apps.organizations.urls')),
    url(r'^projects/', include('academic.apps.projects.urls')),
    url(r'^content/', include('academic.apps.content.urls')),
)
