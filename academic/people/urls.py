from django.conf.urls.defaults import *

from people.models import *

urlpatterns = patterns(
    'django.views.generic',

    url(r'$',
        'list_detail.object_list',
        { 'queryset': Person.visible.all(),
          'allow_empty': False },
        name='people_list'),
)
