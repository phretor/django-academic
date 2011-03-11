from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list, object_detail

from academic.people.models import *

urlpatterns = patterns(
    '',

    url(r'^$',
        cache_page(object_list),
        {'template_name': 'academic/person_list.html',
         'queryset': Person.objects.all(),
         'extra_context': {
                'everyone': Person.objects_all.all().order_by(
                    'last_name').order_by('first_name'),
                'alumni': Person.objects_alumni.all(),
                'visitors': Person.objects_visitors.all(),
                'past_visitors': Person.objects_past_visitors.all()} },
        name='academic_people_person_list'),

    url(r'^\#person-(?P<object_id>\d+)$',
        cache_page(object_list),
        {'template_name': 'academic/person_list.html',
         'queryset': Person.objects.all() },
        name='academic_people_person_detail'),
)
