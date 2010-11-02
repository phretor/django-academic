from django.conf.urls.defaults import *
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list, object_detail

from academic.organizations.models import *

urlpatterns = patterns(
    '',

    url(r'^sponsors/$',
        cache_page(object_list, settings.CACHE_MIDDLEWARE_SECONDS),
        {'template_name': 'academic/sponsor_list.html',
         'queryset': Sponsor.objects.all() },
        name='academic_organizations_sponsor_list'),
)
