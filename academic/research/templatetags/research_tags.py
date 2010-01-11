from django import template

from research.models import *

register = template.Library()


def research_projects(context, latest=5):
    projects = Project.active.all()
    l = len(projects)
    if l != latest and latest > 0:
        projects = projects[0:latest]
    context['projects'] = projects
    return context
register.inclusion_tag('tags/projects.html', takes_context=True)(research_projects)


def research_projects_column(context, latest=5):
    return research_projects(context, latest=latest)
register.inclusion_tag('tags/projects_column.html', takes_context=True)(research_projects_column)


def papers(context, latest=5):
    try:
        object_list = Paper.objects.all()
        l = len(object_list)
        if l != latest and latest > 0:
            object_list = object_list[0:latest]
            context['object_list'] = object_list
    except Paper.DoesNotExist:
        pass
    return context
register.inclusion_tag('tags/research/column.html', takes_context=True)(papers)
