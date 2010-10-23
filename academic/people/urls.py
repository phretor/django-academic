from django.conf.urls.defaults import *
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list, object_detail

from academic.models import *
from academic.views import *

urlpatterns = patterns(
    '',

    url(r'^$',
        cache_page(object_list, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/person_list.html',
         'queryset': Person.objects.all() },
        name='academic_person_list'),
)
