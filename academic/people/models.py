from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from datetime import datetime
from filebrowser.fields import FileBrowseField

class Rank(models.Model):
    """
    The academic rank (e.g., udergraduate student, graduate student,
    phd candidate, assistant professor)
    """
    class Meta:
        verbose_name = _('Rank')
        verbose_name_plural = _('Ranks')
        ordering = ['order']

    name = models.CharField(
        _('Rank name'),
        help_text=_('E.g., Full Professor'),
        max_length=64)
    plural_name = models.CharField(
        _('Rank plural name'),
        help_text=_('E.g., Full Professors'),
        max_length=64,
        blank=True,
        null=True)
    order = models.PositiveSmallIntegerField(
        _('Rank order'),
        help_text=_('Lower values mean higher importance. I.e., 0 should be attributed to "Full professor"'))

    def __unicode__(self):
        return u'%s' % self.plural_name


class VisiblePersonManager(models.Manager):
    """
    Filters people with visible profile.
    """
    def get_query_set(self):
        return super(
            VisiblePersonManager,
            self).get_query_set().filter(published__exact=True)

class Person(models.Model):
    """
    A person in a research lab.
    """
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        ordering = ['rank']

    objects = models.Manager()
    visible = VisiblePersonManager()

    active = models.BooleanField(
        _('Still in the group?'),
        default=True)
    published = models.BooleanField(
        _('Publicly visible?'),
        default=True)
    first_name = models.CharField(
        _('First Name'),
        max_length=64)
    last_name = models.CharField(
        _('Last Name'),
        max_length=64)    
    rank = models.ForeignKey(
        Rank,
        verbose_name=_('Academic Rank'))
    e_mail = models.EmailField(
        _('E-mail'))
    web_page = models.URLField(
        _('Web page'),
        blank=True,
        null=True)
    description = models.TextField(
        _('Description'))
    picture = FileBrowseField(
        _('Profile picture'),
        max_length=200,
        directory='people/person/pictures',
        help_text=_('Will be automatically cropped to 250x300.'),
        format='Image')
    
    def __unicode__(self):
        return u'%s' % self.name

    def _name(self):
        return u'%s %s' % (self.first_name, self.last_name)
    name = property(_name)
