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

from datetime import date

from academic.settings import *
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


class AlumniManager(models.Manager):
    '''
    People who graduated here and left.
    '''
    def get_query_set(self):
        return super(AlumniManager, self).get_query_set().filter(
            alumni=True,
            public=True)


class VisitorManager(models.Manager):
    '''
    People who are visiting.
    '''
    def get_query_set(self):
        return super(VisitorManager, self).get_query_set().filter(
            current=True,
            visitor=True,
            public=True)


class PastVisitorManager(models.Manager):
    '''
    People who visited the lab in the past.
    '''
    def get_query_set(self):
        return super(PastVisitorManager, self).get_query_set().filter(
            visitor=True,
            current=False,
            public=True)


class PersonManager(models.Manager):
    '''
    Genuine people.
    '''
    def get_query_set(self):
        return super(PersonManager, self).get_query_set().filter(
            current=True,
            visitor=False,
            alumni=False,
            public=True)

class Person(models.Model):
    """
    A person in a research lab.
    """
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')
        unique_together = (
            'first_name',
            'mid_name',
            'last_name')
        ordering = [
            'rank',
            'last_name',
            'first_name', ]


    objects_all = models.Manager()
    objects_visitors = VisitorManager()
    objects_alumni = AlumniManager()
    objects_past_visitors = PastVisitorManager()
    objects = PersonManager()
    
    affiliation = models.ManyToManyField(
        Organization,
        verbose_name=_('Affiliations'),
        blank=True,
        null=True,
        related_name='people')
    public = models.BooleanField(
        verbose_name=_('Public?'),
        help_text=_('Toggle visibility on main pages.'),
        default=True)
    visitor = models.BooleanField(
        verbose_name=_('Visitor'),
        help_text=_('Is he/she a visitor?'),
        default=False)
    alumni = models.BooleanField(
        verbose_name=_('Alumni'),
        help_text=_('Did he/she graduate here?'),
        default=False)
    current = models.BooleanField(
        verbose_name=_('Current'),
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
	directory=PEOPLE_DEFAULT_DIRECTORY,
        format='Image',
        default=PEOPLE_DEFAULT_PICTURE,
        blank=True,
        null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('academic_people_person_detail', (), {'object_id': self.pk})

    def _get_picture_url(self):
        if self.has_picture:
            return str(self.picture)
        return PEOPLE_DEFAULT_PICTURE
    picture_url = property(_get_picture_url)

    def photo(self):
        if self.has_picture:
            return '<img src="%s" alt="%s">' % (
                self.picture.url_thumbnail,
                self.name)
        return _('(no photo)')
    photo.allow_tags = True

    def _has_picture(self):
        return not isinstance(self.picture.filesize, str) \
            and self.picture.filesize > 0 \
            and self.picture.filetype_checked == 'Image'
    has_picture = property(_has_picture)

    def __unicode__(self):
        return u'%s' % self.name

    def _get_name(self):
        r = '%s' % self.first_name
        if self.mid_name:
            r = '%s %s.' % (r, self.mid_name[0])
        return '%s %s' % (r, self.last_name)
    name = property(_get_name)

    def _get_fullname(self):
        r = '%s' % self.first_name
        if self.mid_name:
            r = '%s %s' % (r, self.mid_name)
        return '%s %s' % (r, self.last_name)
    fullname = property(_get_fullname)

    def _get_sname(self):
        r = '%s.' % self.first_name[0]
        if self.mid_name:
            r = '%s %s.' % (r, self.mid_name[0])
        return '%s %s' % (r, self.last_name)
    sname = property(_get_sname)

    def _get_slug(self):
        return (u'%s-%s' % (self.first_name[0], self.last_name)).lower()
    slug = property(_get_slug)
