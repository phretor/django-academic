from django import http
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.conf import settings

class PlainTextResponseMixin(TemplateResponseMixin):
    def render_to_response(self, context):
        return super(PlainTextResponseMixin, self).render_to_response(
            context,
            content_type='plain/text; charset=%s' % settings.DEFAULT_CHARSET)

class PlainTextListView(PlainTextResponseMixin, ListView):
    pass

class PlainTextDetailView(PlainTextResponseMixin, DetailView):
    pass
