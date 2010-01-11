from django.conf.urls.defaults import *

from research.models import *

urlpatterns = patterns(
    'django.views.generic',
    
    url(r'papers/$',
        'list_detail.object_list',
        { 'queryset': Paper.objects.all(), 'allow_empty': False },
        name='research_paper_list'),

    url(r'papers/(?P<object_id>\d+)/$',
        'list_detail.object_detail',
        { 'queryset': Paper.objects.all() },
        name='research_paper'),

    url(r'projects/$',
        'list_detail.object_list',
        { 'queryset': Project.objects.all(), 'allow_empty': False },
        name='research_project_list'),

    url(r'projects/(?P<object_id>\d+)/$',
        'list_detail.object_detail',
        { 'queryset': Project.active.all() },
        name='research_project'),
)
