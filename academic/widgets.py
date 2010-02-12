from django.forms.widgets import Select, HiddenInput, TextInput

from yafinder.filters.widgets import Link
from django.utils.safestring import mark_safe

class ListLink(Link):
    def render(self, name, value, attrs=None, choices=()):
        if not choices:
            choices = self.choices
        if value is None:
            value = u""
        # a hidden input with current value is rendered for mantaining
        # current link choice                  
        output = [HiddenInput().render(name, value)]
        # the template for selected choice
        template = u"""<li class="yaselected"><strong>%s</strong></li>"""
        u_template = u"""<li class="yaoption">%s</li>"""
        for k, v in choices:
            if k == value:
                output.append(template % v)
            else:
                output.append(u_template % self._get_link(name, k, v))
        return mark_safe(u"\n".join(output))
        
