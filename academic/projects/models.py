from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from academic.utils import *

from academic.content.models import *
from academic.people.models import *
from academic.publishing.models import *

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
        verbose_name=_('Main topic'),
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
