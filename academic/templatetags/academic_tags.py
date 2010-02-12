from django import template
from django.utils.safestring import mark_safe

from academic.models import *

from form_utils.utils import select_template_from_string

register = template.Library()

@register.filter
def academic_render_person_list(
    object_list,
    template_name='academic/people/includes/person_name.html', context={}):

    return academic_parse_authors(
        ', '.join([p.name for p in object_list]),
        template_name=template_name, context=context)


@register.filter
def academic_parse_authors(
    string, template_name='academic/people/includes/person_name.html', context={}):
    t = select_template_from_string(template_name)

    for p in Person.visible.all():
        if p.name in string:
            string = string.replace(
                p.name, t.render(template.Context({ 'person': p })))

    return mark_safe(string)


def academic_people_list(context, latest=5):
    import random
    try:
        object_list = Person.visible.all()
        l = len(object_list)
        if l != latest and latest > 0:
            object_list = object_list[0:latest]
        random.shuffle(object_list)
        context['object_list'] = object_list
    except Person.DoesNotExist:
        pass
    return context
register.inclusion_tag('academic/templatetags/academic_people_list.html', takes_context=True)(academic_people_list)


def academic_project_list(context, latest=5):
    projects = Project.visible.all()
    l = len(projects)
    if l != latest and latest > 0:
        projects = projects[0:latest]
    context['projects'] = projects
    return context
register.inclusion_tag('academic/templatetags/academic_project_list.html', takes_context=True)(academic_project_list)


def academic_paper_list(context, latest=5):
    try:
        object_list = Paper.visible.all()
        l = len(object_list)
        if l != latest and latest > 0:
            object_list = object_list[0:latest]
            context['object_list'] = object_list
    except Paper.DoesNotExist:
        pass
    return context
register.inclusion_tag('academic/templatetags/academic_paper_list.html', takes_context=True)(academic_paper_list)
