from django.http import HttpResponsePermanentRedirect
from django.template import loader
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_detail

from academic.projects.models import *

def project_detail(
    request, queryset, object_id=None, slug=None,
    slug_field='slug', template_name=None, template_name_field=None,
    template_loader=loader, extra_context=None,
    context_processors=None, template_object_name='object',
    mimetype=None):

    object = get_object_or_404(Project, pk=object_id)

    if object.redirect_to:
       return HttpResponsePermanentRedirect(object.redirect_to)
    
    return object_detail(
        request,
        queryset,
        object_id=object_id,
        slug=slug,
        slug_field=slug_field,
        template_name=template_name,
        template_name_field=template_name_field,
        template_loader=template_loader,
        extra_context=extra_context,
        context_processors=context_processors,
        template_object_name=template_object_name,
        mimetype=mimetype)
