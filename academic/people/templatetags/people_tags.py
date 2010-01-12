from django import template

from people.models import *

import logging

register = template.Library()


def people(context, latest=5):
    import random
    try:
        object_list = Person.objects.filter(active=True, published=True)
        l = len(object_list)
        if l != latest and latest > 0:
            object_list = object_list[0:latest]
        random.shuffle(object_list)
        context['object_list'] = object_list
    except Person.DoesNotExist:
        logging.debug('No people found')
    return context
register.inclusion_tag('templatetags/people.html', takes_context=True)(people)
