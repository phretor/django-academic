from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.text import truncate_html_words
from django.utils.text import truncate_words

from academic.people.models import *

from filebrowser.fields import FileBrowseField
from tagging_autocomplete.models import TagAutocompleteField


class Topic(models.Model):
    """
    A wide-spectrum research topic (e.g., web application security,
    recommendation systems, intrusion detection).
    """
    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    name = models.CharField(
        _('Name'),
        max_length = 256)
    excerpt = models.CharField(
        _('Excerpt'),
        max_length=512,
        help_text=_('A one/two-liner that describes the topic.'),
        blank=True,
        null=True)
    description = models.TextField(
        _('Description'))
    picture = FileBrowseField(
        _('Picture'),
        max_length=200,
        directory='academic/research/topics/pictures',
        format='Image')
    link = models.URLField(
        _('URL'),
        blank=True,
        null=True)
    people = models.ManyToManyField(
        Person,
        verbose_name=_('People Involved'))

    def __unicode__(self):
        return u'%s' % self.name

    def _short_description(self):
        if self.excerpt:
            return self.excerpt
        return truncate_html_words(self.description, 15)
    short_description = property(_short_description)


class ProjectManager(models.Manager):
    """
    Filters the active projects only.
    """
    def get_query_set(self):
        return super(
            ProjectManager,
            self).get_query_set().filter(published__exact=True)


class Project(models.Model):
    """
    A research project (e.g., Ultimate Web Scanner, My IDS), intended
    to embrace several publications, people and one or more topics.
    """
    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['date_published',]
        
    objects = ProjectManager()
    all = models.Manager()

    name = models.CharField(
        _('Name'),
        max_length=64)
    picture = FileBrowseField(
        _('Picture'),
        max_length=200,
        directory='research/projects/pictures',
        format='Image')
    excerpt = models.CharField(
        _('Excerpt'),
        max_length=512,
        help_text=_('A one/two-liner that describes the project.'),
        blank=True,
        null=True)
    description = models.TextField(
        _('Description'))
    topics = models.ManyToManyField(
        Topic,
        related_name='related_projects',
        verbose_name=_('Topics'))
    core_topic = models.ForeignKey(
        Topic,
        related_name='related_for_core_projects',
        verbose_name=_('Core topic'),
        help_text=_('If not specifed, the first one among'
                    ' <strong>Topics</strong> is assumed'))
    people = models.ManyToManyField(
        Person,
        verbose_name=_('People Involved'))
    published = models.BooleanField(
        _('Publicly visible?'),
        default=True)
    date_starts = models.DateField(
        _('Starts on'),
        blank=True,
        null=True)
    date_ends = models.DateField(
        _('Ends on'),
        blank=True,
        null=True)
    date_published = models.DateField(
        _('Published on'))

    def __unicode__(self):
        return u'%s' % self.name

    def _get_short_description(self):
        if self.excerpt:
            return self.excerpt
        return truncate_html_words(self.description, 15)
    short_description = property(_get_short_description)

    def _get_involved_people(self):
        try:
            return self.people.filter(published=True)
        except Person.DoesNotExist:
            pass
        return None
    involved_people = property(_get_involved_people)

    def _short_topics(self):
        return truncate_words(
            ', '.join([str(t) for t in self.topics.all()]), 5)
    short_topics = property(_short_topics)

    def _get_main_topic(self):
        if self.core_topic:
            return self.core_topic
        return self.topics.all().order_by('name')[0]
    main_topic = property(_get_main_topic)

    @models.permalink
    def get_absolute_url(self):
        return ('research_project', (), { 'object_id': self.id })
    

class PaperType(models.Model):
    """
    Paper type (e.g., conference paper, journal paper, workshop paper).
    """
    
    class Meta:
        verbose_name = _('Paper type')
        verbose_name_plural = _('Paper types')

    name = models.CharField(
        _('Category name'),
        max_length=64,
        help_text=_('E.g., conference paper, book chapter, journal paper'))

    def __unicode__(self):
        return u'%s' % self.name


class Paper(models.Model):
    """
    A scientific publication.
    """
    class Meta:
        verbose_name = _('Paper')
        verbose_name_plural = _('Papers')
        ordering = ['year',]
    
    
    title = models.CharField(
        _('Title'),
        max_length=512)
    authors = TagAutocompleteField(
        _('Authors'),
        help_text=_('Autocompleting, comma separated list of authors.'
                    ' If typed nicely, the system will be able to'
                    ' automagically figure out known people. The complete'
                    ' list of authors can be found into the "Tagging"'
                    ' panel, under "Tags".'),
        blank=True,
        null=True)
    known_authors = models.ManyToManyField(
        Person,
        _('Known authors'),
        help_text=_('Collects all the known people that match any authors.'),
        editable=False,
        null=True,
        blank=False)
    abstract = models.TextField(
        _('Abstract'),
        blank=True,
        null=True)
    topics = models.ManyToManyField(
        Topic,
        verbose_name=_('Related Topics'),
        blank=True,
        null=True)
    projects = models.ManyToManyField(
        Project,
        verbose_name=_('Related Projects'),
        blank=True,
        null=True)
    fulltext = FileBrowseField(
        _('Fulltext'),
        max_length=256,
        directory='academic/research/papers/fulltexts',
        format='Document',
        help_text=_('Only PDFs are allowed. Please, be standard'
                    ' and nice to the world!'),
        blank=True,
        null=True)
    presentation = FileBrowseField(
        _('Presentation'),
        max_length=256,
        directory='academic/research/papers/presentations',
        format='Document',
        help_text=_('Only PDFs are allowed. Please, be standard'
                    ' and nice to the world!'),
        blank=True,
        null=True)
    extra_attachment = FileBrowseField(
        _('Extra attachment'),
        max_length=256,
        directory='academic/research/papers/attachments',
        format='File',
        help_text=_('Use this to attach the source code archive'
                    ' or something else.'),
        blank=True,
        null=True)
    notes = models.CharField(
        _('Notes'),
        max_length=512,
        help_text=_('Notes, e.g., about the conference or the journal.'),
        blank=True,
        null=True)
    location = models.CharField(
        _('Location'),
        max_length=512,
        help_text=_('Conference or publisher\'s location.'),
        blank=True,
        null=True)
    details = models.CharField(
        _('Further information'),
        max_length=128,
        help_text=_('Further details such as pages, volume, etc.'),
        blank=True,
        null=True)
    type = models.ForeignKey(
        PaperType,
        verbose_name=_('Paper type'))
    bibtex = models.TextField(
        _('BibTeX Entry'),
        blank=True,
        null=True)
    year = models.PositiveSmallIntegerField(
        _('Year of publication'))
    date_updated = models.DateField(
        _('Last updated on'),
        auto_now=True)
    published = models.BooleanField(
        _('Publicly visible?'),
        default=True)

    @models.permalink
    def get_absolute_url(self):
        return ('research_paper', (), { 'object_id': self.id })

    def _get_downloads(self):
        l = list()
        
        if self.fulltext:
            l.append(self.fulltext)
        if self.presentation:
            l.append(self.presentation)
        if self.extra_attachment:
            l.append(self.extra_attachment)
        
        return l
    downloads = property(_get_downloads)

    def _get_html_id(self):
        return u'paper-%d' % self.id
    html_id = property(_get_html_id)

    def __unicode__(self):
        return u'%s %s' % (
            self.title,
            self.year)

    def _get_smart_authors(self):
        authors = []
        for author in self.authors.replace('  ', ' ').replace(', ', ',').split(','):
            _first_name = None
            _last_name = None
            _author = None
            
            try:
                _first_name = author.split(' ')[0]
                _last_name = author.split(' ')[1]
            except IndexError:
                pass
            
            if _first_name and _last_name:
                try:
                    _author = self.people.filter(
                        first_name=_first_name,
                        last_name=_last_name)[0]
                except (IndexError, Person.DoesNotExist):
                    pass

            if _author:
                authors.append(_author)
            else:
                authors.append(author)
        return authors
    smart_authors = property(_get_smart_authors)
