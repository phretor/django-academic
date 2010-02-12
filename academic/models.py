from django.db import models
from django.utils.translation import ugettext as _
from django.db.models import signals
from django.conf import settings
from django.template.defaultfilters import slugify

from academic.models import *
from profields.fields import *
from settings import COLLABORATION_DIFFICULTIES
from settings import COLLABORATION_TYPES

from tagging_autocomplete.models import TagAutocompleteField
from tagging.models import Tag

from filebrowser.fields import FileBrowseField

from datetime import datetime


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
        help_text=_('Lower values mean higher importance.'
                    ' I.e., 0 should be attributed to "Full professor"'))

    def __unicode__(self):
        return u'%s' % self.plural_name


class PersonManager(models.Manager):
    """
    Retrieve people with visible profile that still in the research group.
    """
    def get_query_set(self):
        return super(
            PersonManager,
            self).get_query_set().filter(
            public__exact=True, active__exact=True, rank__isnull=False)


class AlumniManager(models.Manager):
    """
    Retrieve people with inactive profile (i.e., alumni).
    """
    def get_query_set(self):
        return super(
            AlumniManager,
            self).get_query_set().filter(
            public__exact=True, active__exact=False)


class Person(models.Model):
    """
    A person in a research lab.
    """
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')
        ordering = ['rank']

    objects = models.Manager()
    visible = PersonManager()
    alumni = AlumniManager()

    active = models.BooleanField(
        _('Still in the group?'),
        default=False)
    public = models.BooleanField(
        verbose_name=_('Public?'),
        help_text=_('Toggle visibility on public pages.'),
        default=False)
    first_name = models.CharField(
        _('First Name'),
        max_length=64)
    last_name = models.CharField(
        _('Last Name'),
        max_length=64)    
    rank = models.ForeignKey(
        Rank,
        verbose_name=_('Academic Rank'),
        blank=True,
        null=True,
        related_name='people')
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
        directory='academic/people/person/pictures',
        help_text=_('Will be automatically cropped to 250x300.'),
        format='Image',
        blank=True,
        null=True)
    
    def __unicode__(self):
        return u'%s' % self.name

    def _get_name(self):
        return u'%s %s' % (self.first_name, self.last_name)
    name = property(_get_name)


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
        directory='academic/topics/pictures',
        format='Image')
    link = models.URLField(
        _('URL'),
        blank=True,
        null=True)
    people = models.ManyToManyField(
        Person,
        verbose_name=_('People Involved'),
        related_name='topics')

    def __unicode__(self):
        return u'%s' % self.name

    def _short_description(self):
        if self.excerpt:
            return self.excerpt
        return truncate_html_words(self.description, 15)
    short_description = property(_short_description)


class ProjectManager(models.Manager):
    """
    Show public projects only.
    """
    def get_query_set(self):
        return super(
            ProjectManager,
            self).get_query_set().filter(public__exact=True)


class Project(models.Model):
    """
    A research project (e.g., Ultimate Web Scanner, My IDS), intended
    to embrace several publications, people and one or more topics.
    """
    class Meta:
        verbose_name = _('Funded project')
        verbose_name_plural = _('Funded projects')
        ordering = ['date_published',]

    visible = ProjectManager()
    objects = models.Manager()

    public = models.BooleanField(
        verbose_name=_('Public?'),
        help_text=_('Toggle visibility on public pages.'),
        default=True)
    name = models.CharField(
        _('Name'),
        max_length=64)
    picture = FileBrowseField(
        _('Picture'),
        max_length=200,
        directory='academic/projects/pictures',
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
                    ' <strong>Topics</strong> is assumed'),
        blank=True,
        null=True)
    people = models.ManyToManyField(
        Person,
        verbose_name=_('People Involved'),
        related_name='projects')
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

    def _get_title(self):
        return self.name
    title = property(_get_title)

    def __unicode__(self):
        return u'%s' % self.name

    def _get_short_description(self):
        if self.excerpt:
            return self.excerpt
        return truncate_html_words(self.description, 15)
    short_description = property(_get_short_description)

    def _get_involved_people(self):
        try:
            return self.people.filter(public=True)
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
        return ('academic_project_detail', (), { 'object_id': self.id })
    

class PaperType(models.Model):
    """
    Paper type (e.g., conference paper, journal paper, workshop paper).
    """
    
    class Meta:
        verbose_name = _('Paper type')
        verbose_name_plural = _('Paper types')
        ordering = ('order', )

    name = models.CharField(
        _('Category name'),
        max_length=64,
        help_text=_('E.g., conference paper, book chapter, journal paper'))
    order = models.PositiveSmallIntegerField(
        _('Order of importance'),
        help_text=_('Lower values mean higher importance.'),
        default=0)

    def __unicode__(self):
        return u'%s' % self.name


class PaperManager(models.Manager):
    """
    Show public papers only.
    """
    def get_query_set(self):
        return super(
            PaperManager,
            self).get_query_set().filter(public__exact=True)


class Paper(models.Model):
    """
    A scientific publication.
    """
    class Meta:
        verbose_name = _('Paper')
        verbose_name_plural = _('Papers')
        ordering = ['year',]

    visible = PaperManager()
    objects = models.Manager()

    public = models.BooleanField(
        verbose_name=_('Public?'),
        help_text=_('Toggle visibility on public pages.'),
        default=True)
    title = models.CharField(
        _('Title'),
        max_length=512)
    authors = models.CharField(
        verbose_name=_('Authors'),
        max_length=1024,
        help_text=_(
            'Comma separated list of authors. Will be matched'
            ' against known people if typed accordingly.'
            ' E.g., "First Last" is fine, "F. Last" is bad.'))
    abstract = models.TextField(
        _('Abstract'),
        blank=True,
        null=True)
    topics = models.ManyToManyField(
        Topic,
        verbose_name=_('Related Topics'),
        blank=True,
        null=True,
        related_name='papers')
    projects = models.ManyToManyField(
        Project,
        verbose_name=_('Related Projects'),
        blank=True,
        null=True,
        related_name='papers')
    fulltext = FileBrowseField(
        _('Fulltext'),
        max_length=256,
        directory='academic/papers/fulltexts',
        format='Document',
        help_text=_('Only PDFs are allowed. Please, be standard'
                    ' and nice to the world!'),
        blank=True,
        null=True)
    presentation = FileBrowseField(
        _('Presentation'),
        max_length=256,
        directory='academic/papers/presentations',
        format='Document',
        help_text=_('Only PDFs are allowed. Please, be standard'
                    ' and nice to the world!'),
        blank=True,
        null=True)
    extra_attachment = FileBrowseField(
        _('Extra attachment'),
        max_length=256,
        directory='academic/papers/attachments',
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
        verbose_name=_('Paper type'),
        related_name='papers')
    bibtex = models.TextField(
        verbose_name=_('BibTeX Entry'),
        help_text=_('At this moment, the BibTeX is not parsed for content.'),
        blank=True,
        null=True)
    year = YearField(
        _('Year of publication'))
    date_updated = models.DateField(
        _('Last updated on'),
        auto_now=True)

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


class CourseManager(models.Manager):
    """
    Show public courses only.
    """
    def get_query_set(self):
        return super(
            CourseManager,
            self).get_query_set().filter(public__exact=True)


class Course(models.Model):
    """
    A course such as Math I, Advanced Topics in Information Security.
    """
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    objects = models.Manager()
    visible = CourseManager()

    public = models.BooleanField(
        verbose_name=_('Public?'),
        help_text=_('Toggle visibility on public pages.'),
        default=False)
    title = models.CharField(
        _('Title'),
        max_length=256)
    code = models.CharField(
        _('Code'),
        max_length=16)
    instructors = models.ManyToManyField(
        Person,
        verbose_name=_('Instructors'),
        blank=True,
        null=True,
        related_name='courses_as_instructor')
    assistants = models.ManyToManyField(
        Person,
        verbose_name=_('Assistants'),
        blank=True,
        null=True,
        related_name='courses_as_assistant')
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True)
    date_starts = models.DateField(
        _('Starts on'),
        blank=True,
        null=True)
    date_ends = models.DateField(
        _('Ends on'),
        blank=True,
        null=True)
    link = models.URLField(
        _('Link'),
        blank=True,
        null=True)

    def __unicode__(self):
        return u'%s - %s (%s)' % (
            self.title,
            self.code,
            self.instructor)


class CollaborationProjectManager(models.Manager):
    def get_query_set(self):
        return super(
            CollaborationProjectManager,
            self).get_query_set().filter(
            public__exact=True, type__exact=0)

class CollaborationThesisManager(models.Manager):
    def get_query_set(self):
        return super(
            CollaborationThesisManager,
            self).get_query_set().filter(
            public__exact=True, type__exact=1)

class CollaborationPhdManager(models.Manager):
    def get_query_set(self):
        return super(
            CollaborationPhdManager,
            self).get_query_set().filter(
            public__exact=True, type__exact=2)

class CollaborationJobManager(models.Manager):
    def get_query_set(self):
        return super(
            CollaborationJobManager,
            self).get_query_set().filter(
            public__exact=True, type__exact=3)

class CollaborationManager(models.Manager):
    def get_query_set(self):
        return super(
            CollaborationManager,
            self).get_query_set().filter(
            public__exact=True)
    
class Collaboration(models.Model):
    """
    A collaboration like a thesis, a small project to be assigned to
    one or more persons.
    """
    class Meta:
        verbose_name = _('Collaboration')
        verbose_name_plural = _('Collaborations')

    visible = CollaborationManager()
    projects = CollaborationProjectManager()
    theses = CollaborationThesisManager()
    phds = CollaborationPhdManager()
    jobs = CollaborationJobManager()
    objects = models.Manager()

    type = models.PositiveSmallIntegerField(
        _('Type of collaboration'),
        choices=COLLABORATION_TYPES)
    language = LanguageField(
        verbose_name=_('Language'),
        default='en')
    public = models.BooleanField(
        verbose_name=_('Public?'),
        help_text=_('Toggle visibilty on public pages.'),
        default=True)
    title = models.CharField(
        _('Title'),
        max_length=256)
    assigned_to = models.ManyToManyField(
        Person,
        verbose_name=_('Assigned to'),
        related_name='collaborations',
        blank=True,
        null=True)
    date_assigned = models.DateField(
        _('Assigned on'),
        blank=True,
        null=True)
    date_completed = models.DateField(
        _('Completed on'),
        blank=True,
        null=True)
    date_published = models.DateField(
        _('Published on'))
    date_updated = models.DateField(
        _('Last updated on'),
        auto_now=True)
    description = models.TextField(
        verbose_name=_('Description'))
    status = models.TextField(
        verbose_name=_('Status'),
        help_text=_('How is this work going?'),
        blank=True,
        null=True)
    topics = models.ManyToManyField(
        Topic,
        verbose_name=_('Research topics'))
    related_projects = models.ManyToManyField(
        Project,
        verbose_name=_('Research projects'),
        blank=True,
        null=True,
        related_name='related_theses')
    supervisors = models.ManyToManyField(
        Person,
        verbose_name=_('Supervisors'),
        related_name='collaboration_supervised')
    difficulty = models.PositiveSmallIntegerField(
        _('Expected Difficulty'),
        choices=COLLABORATION_DIFFICULTIES)
    first_download = FileBrowseField(
        verbose_name=_('Downloadable content'),
        max_length=256,
        directory='academic/collaborations/downloads',
        format='Document',
        blank=True,
        null=True)
    second_download = FileBrowseField(
        verbose_name=_('Extra downloadable content'),
        max_length=256,
        directory='academic/collaborations/downloads',
        format='Archive',
        blank=True,
        null=True)
    third_download = FileBrowseField(
        verbose_name=_('Third extra downloadable content'),
        max_length=256,
        directory='academic/collaborations/downloads',
        format='Archive',
        blank=True,
        null=True)
    link = models.URLField(
        verbose_name=_('Link'),
        blank=True,
        null=True)
    skills = TagAutocompleteField(
        _('Required Skill'),
        help_text=_('Autocompleting, comma separated list of skills.'),
        max_length=256,
        blank=True,
        null=True)
    related_collaborations = models.ManyToManyField(
        'self',
        verbose_name=_('Related collaborations'),
        blank=True,
        null=True)
    published_papers = models.ManyToManyField(
        Paper,
        verbose_name=_('Papers published'),
        help_text=_('Papers published within this collaboration.'),
        blank=True,
        null=True)

    def __unicode__(self):
        return u'%s' % self.title

    def _get_assigned(self):
        return self.date_assigned is not None or len(self.assigned_to.all()) > 0
    assigned = property(_get_assigned)

    def _get_completed(self):
        return self.date_completed is not None
    completed = property(_get_completed)
