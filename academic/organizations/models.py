from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from filebrowser.fields import FileBrowseField
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^filebrowser\.fields\.FileBrowseField"])
except:
    pass

from django_countries.fields import CountryField

from academic.utils import *
from academic.settings import *

class Organization(models.Model):
    name = models.CharField(
        _('Name'),
        help_text=_('E.g., Springer, University of California Santa Barbara'),
        max_length=256,
        db_index=True)
    web_page = models.URLField(
        blank=True,
        null=True)
    country = CountryField(
        db_index=True,
        blank=True,
        null=True)
    acronym = models.CharField(
        blank=True,
        null=True,
        max_length=16,
        help_text=_('E.g., UCSB.'),
        validators=[RegexValidator(regex=r'^[A-Za-z]+$')])

    def __unicode__(self):
        return self.name


class Institution(Organization):
    pass


class School(Organization):
    pass


class Publisher(Organization):
    pass

class Sponsor(Organization):
    class Meta:
        ordering = [
            'order',
            'name']
    order = models.PositiveSmallIntegerField(
        help_text='Give important sponsors a lower positive number',
        default=0)
    logo = FileBrowseField(
        _('Logo'),
	directory=SPONSORS_DEFAULT_DIRECTORY,
        max_length=256,
        format='Image',
        blank=True,
        null=True)

    def _has_logo(self):
        return isinstance(self.logo.filesize, int) \
            and self.logo.filesize > 0 \
            and self.logo.filetype_checked == 'Image'
    has_logo = property(_has_logo)
    
    def __unicode__(self):
        return self.title

    def _get_title(self):
        if self.acronym:
            return self.acronym
        return self.name
    title = property(_get_title)
