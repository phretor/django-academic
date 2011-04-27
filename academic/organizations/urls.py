from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView

from academic.organizations.models import *

urlpatterns = patterns(
    '',

    url(r'^sponsors/$',
        cache_page(ListView.as_view(
                template_name='academic/sponsor_list.html',
                model=Sponsor)),
        name='academic_organizations_sponsor_list'),
)
