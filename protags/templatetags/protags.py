from django import template
from form_utils.utils import select_template_from_string
from django.shortcuts import get_object_or_404 as go404

register = template.Library()

@register.filter
def protags_permalink(
    string, template_name='protags/permalink.html', context={}):
    context.update({'string': string})

    t = select_template_from_string(template_name)
    return t.render(template.Context(context))


@register.filter
def protags_object_permalink(
    object, string, template_name='protags/permalink.html'):
    
    context = {}
    try:
        context = {'href': object.get_absolute_url()}
    except:
        pass

    return protags_permalink(string, template_name, context)
