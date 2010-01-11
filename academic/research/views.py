from django.views.generic.list_detail import object_detail
from django.template import loader

from research.models import *

def project_detail(
    request, queryset, object_id=None, slug=None,
    slug_field='slug', template_name=None, template_name_field=None,
    template_loader=loader, extra_context={},
    context_processors=None, template_object_name='object',
    mimetype=None):
    
    extra_context.update({ 'related_projects': Project.objects.all() })

    return object_detail(
        request,
        queryset,
        object_id=object_id,
        slug=slug,
        slug_field=slug_field,
        template_name=template_name,
        template_loader=template_loader,
        extra_context=extra_context,
        context_processors=context_processors,
        template_object_name=template_object_name,
        mimetype=mimetype)
