from django.views.generic.list_detail import object_list
from django.utils.translation import ugettext as _
from django.template import loader
from django.shortcuts import get_object_or_404

from academic.models import *
from academic.widgets import *

from yafinder import filters
from yafinder import sorters

def paper_object_list(
    request, queryset, paginate_by=None, page=None,
    allow_empty=True, template_name=None, template_loader=loader,
    extra_context=None, context_processors=None, template_object_name='object',
    mimetype=None):

    filter_form = filters.FilterForm(
        (
            filters.LinkField(
                widget=ListLink(),
                allow_none=_(u'All'),
                choices=map(
                    lambda x:(str(x[0]), x[1]),
                    PaperType.objects.values_list('id', 'name')),
                callback=filters.lookup_for('type__id')),
            ),
        data=request.GET)
    
    sorter = sorters.Sorter(
        (
            sorters.Field(
                label=_(u'Publication year'),
                desc=True,
                is_default=True,
                callback=sorters.from_fields('year')),
            ),
        label=_(u'Order by'),
        data=request.GET)

    
    if sorter.is_valid():
        queryset = sorter.run(queryset)
        try:
            extra_context['sorter'] = sorter
        except:
            extra_context = { 'sorter': sorter }
    else:
        return sorter.redirect()


    if filter_form.is_valid():
        queryset = filter_form.run(queryset)
        try:
            extra_context['filter_form'] = filter_form
        except:
            extra_context = { 'filter_form': filter_form }
    else:
        return filter_form.redirect()

    
    return object_list(
        request,
        queryset,
        paginate_by=paginate_by,
        page=page,
        allow_empty=allow_empty,
        template_name=template_name,
        template_loader=template_loader,
        extra_context=extra_context,
        context_processors=context_processors,
        template_object_name=template_object_name,
        mimetype=mimetype)
