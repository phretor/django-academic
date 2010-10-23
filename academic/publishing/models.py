from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from filebrowser.fields import FileBrowseField
from django_countries.fields import CountryField

from academic.utils import *
from academic.people.models import *
from academic.organizations.models import *

class Conference(models.Model):
    class Meta:
        ordering = [
            'acronym',
            'name', ]
        
    name = models.CharField(
        _('Name'),
        help_text=_('E.g., Recent Advances in Intrusion Detection'),
        max_length=256,
        unique=True,
        db_index=True)
    acronym = models.CharField(
        blank=True,
        null=True,
        max_length=16,
        help_text=_('E.g., RAID.'),
        validators=[RegexValidator(regex=r'^[A-Za-z]+$')])

    def __unicode__(self):
        return self.acronym or self.name


class ConferenceEdition(models.Model):
    class Meta:
        ordering = [
            '-year',
            '-month',
            'conference__acronym',
            'conference__name',]
    conference = models.ForeignKey(
        Conference)
    month = models.PositiveSmallIntegerField(
        choices=MONTHS,
        blank=True,
        null=True,
        db_index=True)
    year = models.CharField(
        max_length=4,
        choices=YEARS,
        help_text=_('Year of the event'),
        db_index=True)
    address = models.TextField(
        _('Address'),
        help_text=_('Conference location.'),
        blank=True,
        null=True)
    web_page = models.URLField(
        _('Web page'),
        blank=True,
        null=True)

    def __unicode__(self):
        return u'%s %s' % (self.conference, self.year)

class Publication(models.Model):
    """
    A scientific publication.
    """
    class Meta:
        verbose_name = _('Publication')
        verbose_name_plural = _('Publications')
        ordering = ['year',]

    nickname = models.CharField(
        max_length=16,
        help_text=_(
            'A mnemonic name that "idenfies" this publication.'\
                ' E.g., concept_drift. (lowcase letters and dashes only)'),
        validators=[RegexValidator(regex=r'^[a-z]+(_[a-z]+)*$')])
    title = models.CharField(
        _('Title'),
        max_length=1024)
    year = models.CharField(
        max_length=4,
        choices=YEARS,
        help_text=_('Year of publication'),
        db_index=True)
    month = models.PositiveSmallIntegerField(
        choices=MONTHS,
        db_index=True,
        null=True,
        blank=True)
    authors = models.ManyToManyField(
        'academic.people.Person',
        related_name='publications',
        blank=True,
        null=True)
    attachment = FileBrowseField(
        _('Attachment'),
        max_length=256,
        format='File',
        blank=True,
        null=True)
    notes = models.CharField(
        _('Notes'),
        max_length=512,
        help_text=_('Notes, e.g., about the conference or the journal.'),
        blank=True,
        null=True)
    bibtex = models.TextField(
        verbose_name=_('BibTeX Entry'),
        help_text=_('At this moment, the BibTeX is not parsed for content.'),
        blank=True,
        null=True)
    abstract = models.TextField(
        _('Abstract'),
        blank=True,
        null=True)
    fulltext = FileBrowseField(
        _('Fulltext'),
        max_length=256,
        format='Document',
        blank=True,
        null=True)
    date_updated = models.DateField(
        _('Last updated on'),
        auto_now=True,
        db_index=True)
    citation_key = models.SlugField(
        max_length=512,
        editable=False,
        db_index=True)

    @models.permalink
    def get_absolute_url(self):
        return ('publication', (), { 'object_id': self.id })

    def __unicode__(self):
        return u'%s %s' % (
            self.title,
            self.year)


class Book(Publication):
    editors = models.ManyToManyField(
        'academic.people.Person',
        related_name='proceedings',
        blank=True,
        null=True)
    publisher = models.ForeignKey(
        'academic.organizations.Publisher',
        related_name='books',
        blank=True,
        null=True)
    volume = models.CharField(
        max_length=128,
        blank=True,
        null=True)
    number = models.CharField(
        max_length=128,
        blank=True,
        null=True)
    address = models.TextField(
        _('Address'),
        help_text=_('Conference location.'),
        blank=True,
        null=True)
    edition = models.CharField(
        max_length=128,
        blank=True,
        null=True)

class Journal(Book):
    pass


class BookChapter(Book):
    chapter = models.CharField(
        max_length=128)
    pages = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        help_text=_('E.g., 12-20'),
        validators=[RegexValidator(regex=r'[0-9]+\-[0-9]+')])


class JournalArticle(Publication):
    journal = models.ForeignKey(
        Journal)

class ConferenceProceedings(Book):
    class Meta:
        verbose_name_plural = _('Conference proceedings')
    conference_edition = models.ForeignKey(
        ConferenceEdition)

    def __unicode__(self):
        return u'%s %s (proceedings)' % (self.title, self.year)


class ConferenceArticle(Publication):
    presentation = FileBrowseField(
        _('Presentation'),
        max_length=256,
        format='Document',
        blank=True,
        null=True)
    crossref = models.ForeignKey(
        ConferenceProceedings,
        null=True,
        blank=True)


class TechnicalReport(Publication):
    institution = models.ManyToManyField(
        'academic.organizations.Institution')


class Thesis(Publication):
    school = models.ForeignKey(
        'academic.organizations.School')


class MasterThesis(Thesis):
    class Meta:
        verbose_name_plural = 'Master theses'
        verbose_name = 'Master thesis'
    pass


class PhdThesis(Thesis):
    class Meta:
        verbose_name_plural = 'PhD theses'
        verbose_name = 'PhD thesis'
