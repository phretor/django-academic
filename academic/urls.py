from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

from academic.models import *

urlpatterns = patterns(
    'academic.views',
    
    # papers
    url(r'papers/$',
        'paper_object_list',
        { 'queryset': Paper.visible.all(),
          'template_name': 'academic/papers/paper_list.html' },
        name='academic_paper_list'),
)

urlpatterns += patterns(
    'django.views.generic',


    # people
    url(r'people/$',
        'list_detail.object_list',
        { 'queryset': Person.visible.all(),
          'template_name': 'academic/people/person_list.html' },
        name='academic_people_list'),


    # collaborations
    url(r'collaborations/projects/$',
        'list_detail.object_list',
        { 'queryset': Collaboration.projects.all(),
          'template_name': 'academic/collaborations/project_list.html' },
        name='academic_collaboration_project_list'),

    url(r'collaborations/theses/$',
        'list_detail.object_list',
        { 'queryset': Collaboration.theses.all(),
          'template_name': 'academic/collaborations/thesis_list.html' },
        name='academic_collaboration_thesis_list'),

    url(r'collaborations/phds/$',
        'list_detail.object_list',
        { 'queryset': Collaboration.phds.all(),
          'template_name': 'academic/collaborations/phd_list.html' },
        name='academic_collaboration_phd_list'),

    url(r'collaborations/jobs/$',
        'list_detail.object_list',
        { 'queryset': Collaboration.jobs.all(),
          'template_name': 'academic/collaborations/job_list.html' },
        name='academic_collaboration_jobs_list'),

    
    # projects
    url(r'projects/$',
        'list_detail.object_list',
        { 'queryset': Project.visible.all(),
          'template_name': 'academic/projects/project_list.html' },
        name='academic_project_list'),
    
    url(r'projects/(?P<object_id>\d+)/$',
        'list_detail.object_detail',
        { 'queryset': Project.visible.all(),
          'template_name': 'academic/projects/project_detail.html' },
        name='academic_project_detail'),
)
