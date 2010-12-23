from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField

from model_utils.models import InheritanceCastModel
from filebrowser.fields import FileBrowseField
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^filebrowser\.fields\.FileBrowseField"])
except:
    pass

from academic.settings import *
from academic.utils import *
from academic.organizations.models import *
from academic.people.models import *


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
        max_length=16,
        unique=True,
        help_text=_('E.g., RAID, IMC, EC2ND, CCS, SSP'),
        validators=[RegexValidator(regex=r'^([0-9A-Za-z]+[ ]?)+$')])

    def __unicode__(self):
        return self.name

    def _get_acronymized(self):
        return u'%s (%s %s)' % (
            self.name,
            self.acronym)
    acronymized = property(_get_acronymized)


class ConferenceEdition(models.Model):
    class Meta:
        ordering = [
            '-year',
            '-month',
            'conference__acronym',
            'conference__name',]
        unique_together = (
            'conference',
            'year',)
    
    conference = models.ForeignKey(
        Conference)
    edition_number = models.PositiveSmallIntegerField(
        help_text=_('E.g., "13" as in "Proceedings of the 13th Symposioum on ..."'),
        blank=True,
        null=True,
        db_index=True)
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
        _('Venue'),
        help_text=_('Conference location.'),
        blank=True,
        null=True)
    web_page = models.URLField(
        _('Web page'),
        blank=True,
        null=True)
    slug = models.SlugField(
        max_length=512,
        editable=False,
        db_index=True)

    def __unicode__(self):
        return u'%s %s' % (self.conference, self.year)

    def _get_acronymized(self):
        return u'%s (%s %s)' % (
            self.conference.name,
            self.conference.acronym,
            self.year)
    acronymized = property(_get_acronymized)

    def save(self, **kwargs):
        if len(self.slug) == 0:
            self.slug = slugify('%s %s' % (self.conference.acronym, self.year))
        super(ConferenceEdition, self).save(**kwargs)


class Publication(InheritanceCastModel):
    """
    A scientific publication.
    """
    
    class Meta:
        unique_together = (
            ('title',
             'year'), )
        verbose_name = _('Publication')
        verbose_name_plural = _('Publications')
        ordering = ['-year',]
    
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
        Person,
        related_name='publications',
        through='Authorship',
        blank=True,
        null=True)
    attachment = FileBrowseField(
        _('Attachment'),
	directory=PUBLISHING_DEFAULT_DIRECTORY,
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
        help_text=_(
            'At this moment, the BibTeX is not parsed for content.'\
                'This will override the auto-generated BibTeX.'),
        blank=True,
        null=True)
    abstract = models.TextField(
        _('Abstract'),
        blank=True,
        null=True)
    fulltext = FileBrowseField(
        _('Fulltext'),
	directory=PUBLISHING_DEFAULT_DIRECTORY,
        max_length=256,
        format='Document',
        blank=True,
        null=True)
    date_updated = models.DateField(
        _('Last updated on'),
        auto_now=True,
        db_index=True)
    slug = models.SlugField(
        help_text=_('This is autofilled, then you may modify it if you wish.'),
        editable=False,
        unique=True,
        max_length=512,
        db_index=True)

    def _get_first_author(self):
        authorships = self.authorship_set.all()
        if authorships.count() > 0:
            return authorships[0].person
        return None
    first_author = property(_get_first_author)

    def _get_author_list(self):
        author_list = ', '.join(map(
                lambda m:m.person.name , self.authorship_set.all()))
        return author_list
    author_list = property(_get_author_list)

    @models.permalink
    def get_bibtex_url(self):
        return ('academic_publishing_publication_detail_bibtex', (), {
                'slug': self.slug})

    @models.permalink
    def get_absolute_url(self):
        return ('academic_publishing_publication_detail', (), {'slug': self.slug})

    def __unicode__(self):
        return u'%s %s' % (
            self.title,
            self.year)

    def save(self, *args, **kwargs):
        if len(self.slug) == 0:
            self.slug = slugify('%s %s %s' % (
                    self.first_author or '',
                    self.title,
                    self.year))
        super(Publication, self).save(**kwargs)


class Authorship(models.Model):
    class Meta:
        ordering = ('order',)
    person = models.ForeignKey(Person)
    publication = models.ForeignKey(Publication)
    order = models.PositiveSmallIntegerField()
    

class Book(Publication):
    editors = models.ManyToManyField(
        Person,
        related_name='proceedings',
        through='Editorship',
        blank=True,
        null=True)
    publisher = models.ForeignKey(
        Publisher,
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
        null=True,
        help_text=_('E.g., First, Second, II, 2, Second edition.'))


class Editorship(models.Model):
    class Meta:
        ordering = ('order',)
    person = models.ForeignKey(Person)
    publication = models.ForeignKey(Book)
    order = models.PositiveSmallIntegerField()


class Journal(Book):
    def save(self, *args, **kwargs):
        self.subclass = 'Journal'
        super(Journal, self).save()


class BookChapter(Book):
    chapter = models.CharField(
        max_length=128)
    pages = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        help_text=_('E.g., 12-20'),
        validators=[RegexValidator(regex=r'[0-9]+\-[0-9]+')])

    def save(self, *args, **kwargs):
        self.subclass = 'BookChapter'
        super(BookChapter, self).save()


class JournalArticle(Publication):
    class Meta:
        verbose_name_plural = _('Journal papers')
        verbose_name = _('Journal paper')
    
    journal = models.ForeignKey(
        Journal)


class ConferenceProceedings(Book):
    class Meta:
        verbose_name = _('Proceedings')
        verbose_name_plural = _('Proceedings')
    conference_edition = models.ForeignKey(
        ConferenceEdition)

    def __unicode__(self):
        return u'%s %s (proceedings)' % (
            self.title, self.year)


class ConferenceArticle(Publication):
    class Meta:
        verbose_name_plural = _('Conference papers')
        verbose_name = _('Conference paper')
    presentation = FileBrowseField(
        _('Presentation'),
	directory=PUBLISHING_DEFAULT_DIRECTORY,
        max_length=256,
        format='Document',
        blank=True,
        null=True)
    crossref = models.ForeignKey(
        ConferenceProceedings,
        verbose_name=_('Conference proceedings'),
        null=True,
        blank=True)


class TechnicalReport(Publication):
    institution = models.ManyToManyField(
        Institution)


class Thesis(Publication):
    school = models.ForeignKey(
        School)
    advisors = models.ManyToManyField(
        Person,
        through='Advisorship',
        related_name='advised_theses')
    co_advisors = models.ManyToManyField(
        Person,
        through='Coadvisorship',
        blank=True,
        null=True,
        related_name='coadvised_theses')


class Advisorship(models.Model):
    class Meta:
        ordering = ('order',)
    person = models.ForeignKey(Person)
    publication = models.ForeignKey(Thesis)
    order = models.PositiveSmallIntegerField()


class Coadvisorship(models.Model):
    class Meta:
        ordering = ('order',)
    person = models.ForeignKey(Person)
    publication = models.ForeignKey(Thesis)
    order = models.PositiveSmallIntegerField()


class MasterThesis(Thesis):
    class Meta:
        verbose_name_plural = 'Master theses'
        verbose_name = 'Master thesis'
    pass


class PhdThesis(Thesis):
    class Meta:
        verbose_name_plural = _('PhD theses')
        verbose_name = _('PhD thesis')
    reviewers = models.ManyToManyField(
        Person,
        through='Reviewing',
        related_name='reviewed_phdtheses',
        blank=True,
        null=True)


class Reviewing(models.Model):
    person = models.ForeignKey(Person)
    publication = models.ForeignKey(PhdThesis)
    order = models.PositiveSmallIntegerField()
