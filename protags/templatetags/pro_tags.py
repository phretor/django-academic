from django import template
from django.contrib.sites.models import Site
from django.template import loader, Node, Variable
from django.utils.encoding import smart_str, smart_unicode
from django.template.defaulttags import url
from django.template import VariableDoesNotExist
from django.forms import Form

from protags.settings import PROTOCOL
from protags.settings import LOGIN_FORM_CLASS
from protags.settings import GMAPS_URL
from protags.settings import SANITIZE_ALLOWED_TAGS

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


@register.filter
def protags_shorten(string, length=20):
    if len(string) > length:
        if length <= 3:
            try:
                return string[0:length]
            except:
                pass
        try:
            return string[:length-3].strip() + '...' + string[-3:].strip()
        except:
            pass
    return string


@register.filter
def protags_sanitize(value, allowed_tags=SANITIZE_ALLOWED_TAGS):
    """
    Call this tag like:

      protags_sanitize "content" "tag2 tag4 tag3"

    where tagsare allowed HTML tags, and attrs are the allowed
    attributes for that tag.
    """
    from lxml.html.clean import Cleaner

    kwargs = {
        'add_nofollow': True,
        'style': True }

    if isinstance(allowed_tags, str):
        if allowed_tags is not '':
            try:
                whitelist_tags = set(allowed_tags.split(' '))
            except:
                whitelist_tags = None
            if whitelist_tags is not None:
                kwargs['whitelist_tags'] = whitelist_tags

    c = Cleaner(**kwargs)
    return c.clean_html(value)


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


def delete_confirm_form(context):
    context['form'] = Form()
    return context
register.inclusion_tag(
    'protags/delete_confirm_form.html', takes_context=True)(delete_confirm_form)


@register.tag
def breadcrumb(parser, token):
	"""
        Thanks to: http://www.djangosnippets.org/snippets/1289/

	Renders the breadcrumb.
	Examples:
		{% breadcrumb "Title of breadcrumb" url_var %}
		{% breadcrumb context_var  url_var %}
		{% breadcrumb "Just the title" %}
		{% breadcrumb just_context_var %}

	Parameters:
	-First parameter is the title of the crumb,
	-Second (optional) parameter is the url variable to link to,
         produced by url tag, i.e.:
		{% url person_detail object.id as person_url %}
		then:
		{% breadcrumb person.name person_url %}

	@author Andriy Drozdyuk
	"""
	return BreadcrumbNode(token.split_contents()[1:])


@register.tag
def breadcrumb_url(parser, token):
    """
    Thanks to: http://www.djangosnippets.org/snippets/1289/

    Same as breadcrumb
    but instead of url context variable takes in all the
    arguments URL tag takes.
            {% breadcrumb "Title of breadcrumb" person_detail person.id %}
            {% breadcrumb person.name person_detail person.id %}
    """

    bits = token.split_contents()
    if len(bits)==2:
        return breadcrumb(parser, token)

    # Extract our extra title parameter
    title = bits.pop(1)
    token.contents = ' '.join(bits)

    url_node = url(parser, token)

    return UrlBreadcrumbNode(title, url_node)


class BreadcrumbNode(Node):
    """
    Thanks to: http://www.djangosnippets.org/snippets/1289/
    """
    def __init__(self, vars):
        """
        First var is title, second var is url context variable
        """
        self.vars = map(Variable,vars)

    def render(self, context):
        title = self.vars[0].var

        if title.find("'")==-1 and title.find('"')==-1:
            try:
                val = self.vars[0]
                title = val.resolve(context)
            except:
                title = ''

        else:
            title=title.strip("'").strip('"')
            title=smart_unicode(title)

        url = None

        if len(self.vars)>1:
            val = self.vars[1]
            try:
                url = val.resolve(context)
            except VariableDoesNotExist:
                print 'URL does not exist', val
                url = None

        return create_crumb(title, url)


class UrlBreadcrumbNode(Node):
    """
    Thanks to: http://www.djangosnippets.org/snippets/1289/
    """
    def __init__(self, title, url_node):
        self.title = Variable(title)
        self.url_node = url_node

    def render(self, context):
        title = self.title.var

        if title.find("'")==-1 and title.find('"')==-1:
            try:
                val = self.title
                title = val.resolve(context)
            except:
                title = ''
        else:
            title=title.strip("'").strip('"')
            title=smart_unicode(title)

        url = self.url_node.render(context)
        return create_crumb(title, url)


def create_crumb(title, url=None):
    """
    Thanks to: http://www.djangosnippets.org/snippets/1289/

    Helper function
    """
    crumb = '<span class="breadcrumbs-arrow">&rsaquo;</span>'
    if url:
        crumb = '%s<a href="%s">%s</a>' % (crumb, url, title)
    else:
        crumb = '%s%s' % (crumb, title)

    return crumb
