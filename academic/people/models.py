from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from filebrowser.fields import FileBrowseField
from django_countries.fields import CountryField

from datetime import date

from academic.utils import *

from academic.organizations.models import *

class Rank(models.Model):
    """
    The academic rank (e.g., udergraduate student, graduate student,
    phd candidate, assistant professor)
    """
    class Meta:
        verbose_name = _('Rank')
        verbose_name_plural = _('Ranks')
        ordering = [
            'order',]

    name = models.CharField(
        _('Rank name'),
        help_text=_('E.g., Full Professor'),
        max_length=64)
    plural_name = models.CharField(
        _('Rank plural name'),
        help_text=_('E.g., Full Professors'),
        max_length=64)
    order = models.PositiveSmallIntegerField(
        _('Rank order'),
        help_text=_('Lower values mean higher importance.'
                    ' I.e., put 0 for a "Full professor"'))

    def __unicode__(self):
        return self.name


class Person(models.Model):
    """
    A person in a research lab.
    """
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')
        ordering = [
            'rank',
            'last_name',
            'first_name', ]

    affiliation = models.ManyToManyField(
        Organization,
        verbose_name=_('Affiliations'),
        blank=True,
        null=True,
        related_name='people')
    public = models.BooleanField(
        verbose_name=_('Public?'),
        help_text=_('Toggle visibility on public pages.'),
        default=True)
    current = models.BooleanField(
        help_text=_('Is he/she still in the group?'),
        default=True)
    rank = models.ForeignKey(
        Rank,
        verbose_name=_('Academic Rank'),
        help_text=_('Leave blank if this person is not in the group anymore.'),
        related_name='people',
        blank=True,
        null=True)
    first_name = models.CharField(
        _('First Name'),
        max_length=64)
    mid_name = models.CharField(
        blank=True,
        null=True,
        max_length=64)
    last_name = models.CharField(
        _('Last Name'),
        max_length=64)
    e_mail = models.EmailField(
        _('E-mail'),
        blank=True,
        null=True)
    web_page = models.URLField(
        _('Web page'),
        blank=True,
        null=True)
    description = models.TextField(
        _('Short bio'),
        blank=True,
        null=True)
    picture = FileBrowseField(
        _('Profile picture'),
        max_length=200,
        format='Image',
        blank=True,
        null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('academic_people_person_detail', (), {'object_id': self.pk})

    def _has_picture(self):
        return self.picture != ''
    has_picture = property(_has_picture)

    def __unicode__(self):
        return u'%s' % self.name

    def _get_name(self):
        return u'%s %s' % (self.first_name, self.last_name)
    name = property(_get_name)

    def _get_slug(self):
        return (u'%s-%s' % (self.first_name[0], self.last_name)).lower()
    slug = property(_get_slug)
