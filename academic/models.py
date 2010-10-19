from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS as _MONTHS
from django.core.validators import RegexValidator

from filebrowser.fields import FileBrowseField
from django_countries.fields import CountryField

YEARS = map(lambda x: (str(x), str(x)), range(1960, date.today().year + 10))
MONTHS = map(lambda x: (x[0], x[1]), _MONTHS.items())

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
        max_length=64)
    order = models.PositiveSmallIntegerField(
        _('Rank order'),
        help_text=_('Lower values mean higher importance.'
                    ' I.e., put 0 for a "Full professor"'))

    def __unicode__(self):
        return self.name

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
        max_length=256,
        format='Image',
        blank=True,
        null=True)
    
    def __unicode__(self):
        return self.name

    def _get_title(self):
        if self.acronym:
            return self.acronym
        return self.name
    title = property(_get_title)


class Person(models.Model):
    """
    A person in a research lab.
    """
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')
        ordering = [
            'rank',
            'last_name', ]

    affiliation = models.ManyToManyField(
        Organization,
        blank=True,
        null=True,
        related_name='people')
    public = models.BooleanField(
        verbose_name=_('Public?'),
        help_text=_('Toggle visibility on public pages.'),
        default=False)
    current = models.BooleanField(
        help_text=_('Is he/she still in the group?'),
        default=True)
    rank = models.ForeignKey(
        Rank,
        verbose_name=_('Academic Rank'),
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
        _('Description'),
        blank=True,
        null=True)
    picture = FileBrowseField(
        _('Profile picture'),
        max_length=200,
        format='Image',
        blank=True,
        null=True)
    
    def __unicode__(self):
        return u'%s' % self.name

    def _get_name(self):
        return u'%s %s' % (self.first_name, self.last_name)
    name = property(_get_name)


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
        Person,
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
        Person,
        related_name='proceedings',
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
        Institution)


class Thesis(Publication):
    school = models.ForeignKey(
        School)


class MasterThesis(Thesis):
    class Meta:
        verbose_name_plural = 'Master theses'
        verbose_name = 'Master thesis'
    pass


class PhdThesis(Thesis):
    class Meta:
        verbose_name_plural = 'PhD theses'
        verbose_name = 'PhD thesis'


class HighlightedTopicManager(models.Manager):
    def get_query_set(self):
        return super(HighlightedTopicManager, self).get_query_set().filter(
            highlight=True).order_by('title').order_by('highlight_order')


class Topic(models.Model):
    class Meta:
        ordering = [
            'highlight_order',
            'title']

    objects = models.Manager()
    highlighted = HighlightedTopicManager()
    
    highlight = models.BooleanField(
        default=False,
        help_text='Show this topic on the home page?',
        db_index=True)
    highlight_order = models.PositiveSmallIntegerField(
        default=0,
        help_text='In what order do you want this to be added on the home page?'\
            ' Leave blank for alphabetic order.',
        db_index=True)
    title = models.CharField(
        max_length=2048,
        db_index=True)
    excerpt = models.TextField(
        null=True,
        blank=True)
    description = models.TextField()

    def _get_content(self):
        if self.excerpt:
            return self.excerpt
        return self.description
    content = property(_get_content)

    @models.permalink
    def get_absolute_url(self):
        return ('academic_topic_detail', (), {'object_id': self.pk})

    def __unicode__(self):
        return self.title


class HighlightedProjectManager(models.Manager):
    def get_query_set(self):
        return super(HighlightedProjectManager, self).get_query_set().filter(
            highlight=True)

class Download(models.Model):
    class Meta:
        ordering = [
            'title', ]
    
    title = models.CharField(
        max_length=256)
    description = models.TextField(
        blank=True,
        null=True)
    file = FileBrowseField(
        _('File'),
        max_length=256,
        format='Document',
        blank=True,
        null=True)

    def __unicode__(self):
        return u'%s%s' % (self.title, self.file)

class Project(models.Model):
    class Meta:
        ordering = [
            'topic',
            'modified',
            'created']

    objects = models.Manager()
    highlighted = HighlightedProjectManager()
    
    highlight = models.BooleanField(
        help_text='Highlight this in the projects\' main page?'\
            ' Only the most recently modified one will be displayed.')
    redirect_to = models.URLField(
        blank=True,
        null=True,
        help_text='Use this for old or extenal projects.')
    short_title = models.CharField(
        max_length=1024,
        db_index=True)
    title = models.CharField(
        max_length=2048,
        db_index=True)
    created = models.DateTimeField(
        auto_now_add=True)
    modified = models.DateTimeField(
        auto_now=True)
    excerpt = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        help_text='Concise description to show in the listing page.')
    description = models.TextField(
        null=True,
        blank=True,
        help_text='This content will be rendered right after the title.')
    downloads = models.ManyToManyField(
        Download,
        null=True,
        blank=True,
        help_text='Downloadable files')
    footer = models.TextField(
        null=True,
        blank=True,
        help_text='This content will be rendered at the bottom of the page.')
    people = models.ManyToManyField(
        Person,
        help_text='People involved in this project.',
        related_name='projects')
    organizations = models.ManyToManyField(
        Organization,
        help_text='Organizations involved other than the lab.',
        blank=True,
        null=True,
        related_name='projects')
    publications = models.ManyToManyField(
        Publication,
        blank=True,
        null=True)
    topic = models.ForeignKey(
        Topic,
        help_text='This is the main topic.',
        related_name='projects')
    sponsors = models.ManyToManyField(
        Sponsor,
        blank=True,
        null=True,
        help_text='sponsored_projects')
    related_topics = models.ManyToManyField(
        Topic,
        null=True,
        blank=True,
        help_text='Optional related topics.',
        related_name='secondary_projects')

    def __unicode__(self):
        return self.short_title

    @models.permalink
    def get_absolute_url(self):
        return ('academic_project_detail', (), {'object_id': self.pk})
