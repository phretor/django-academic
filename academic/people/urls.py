from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list
from django.views.generic.list import ListView

from academic.people.models import *

urlpatterns = patterns(
    '',

    # for some reason, switching to class-based views causes crazy
    # things with {{ object_list|regroup }}. Thus, let's stick to the
    # old approach for now.
    url(r'^$',
        cache_page(object_list),
        {'template_name': 'academic/person_list.html',
         'queryset': Person.objects.all(),
         'extra_context': {
                'alumni': Person.objects_alumni.all(),
                'visitors': Person.objects_visitors.all().order_by('rank'),
                'past_visitors': Person.objects_past_visitors.all().order_by('rank')} },
        name='academic_people_person_list'),

    url(r'^\#person-(?P<object_id>\d+)$',
        cache_page(ListView.as_view(
                template_name='academic/person_list.html',
                model=Person)),
        name='academic_people_person_detail'),
)
