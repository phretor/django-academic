from django import template
from django.contrib.sites.models import Site

from protags.settings import PROTOCOL
from protags.settings import LOGIN_FORM_CLASS
from protags.settings import GMAPS_URL

from form_utils.utils import select_template_from_string

register = template.Library()

from django.conf import settings

def get_class(path):
    klass = path.split('.')[-1]
    mod = path.replace('.%s' % klass, '')
    return getattr(__import__(mod, globals(), locals(), [klass, ]), klass)


@register.filter
def protags_permalink(
    string, template_name='protags/permalink.html', context={}):
    context.update({'string': string})

    t = select_template_from_string(template_name)
    return t.render(template.Context(context))


@register.simple_tag
def protags_settings(key):
    try:
        return getattr(settings, key, settings.TEMPLATE_STRING_IF_INVALID)
    except:
        return settings.TEMPLATE_STRING_IF_INVALID


@register.simple_tag
def protags_gmap(query):
    try:
        return GMAPS_URL % { 'query': query }
    except:
        return settings.TEMPLATE_STRING_IF_INVALID

@register.filter
def protags_object_permalink(
    object, string, template_name='protags/permalink.html'):
    
    domain = None
    try:
        domain = Site.objects.get_current().domain
    except:
        pass

    context = {}
    try:
        context = { 'href': object.get_absolute_url() }
    except:
        pass

    if context.has_key('href') and domain is not None:
        context['href'] = '%s://%s%s' % (PROTOCOL, domain, context['href'])

    return protags_permalink(string, template_name, context)


def login_form(context):
    context['form'] = get_class(LOGIN_FORM_CLASS)()
    return context
register.inclusion_tag(
    'protags/login_form.html', takes_context=True)(login_form)
