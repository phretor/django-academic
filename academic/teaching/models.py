from django.db import models
from django.utils.translation import ugettext as _
from django.db.models import signals

from people.models import *
from research.models import *
from assets.models import *
from teaching import config

from tagging_autocomplete.models import TagAutocompleteField

class CourseManager(models.Manager):
    """
    Filters the active courses only.
    """
    def get_query_set(self):
        return super(
            CourseManager,
            self).get_query_set().filter(active__exact=True)


class Course(models.Model):
    """
    A course such as Math I, Advanced Topics in Information Security.
    """
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    objects = CourseManager()
    all = models.Manager()

    title = models.CharField(
        _('Title'),
        max_length=256)
    code = models.CharField(
        _('Code'),
        max_length=16)
    instructors = TagAutocompleteField(
        _('Instructors'),
        help_text=_('Autocompleting, comma separated list of instructors.'
                    ' If typed nicely, the system will be able to'
                    ' automagically figure out known people. The complete'
                    ' list of instructors can be found into the "Tagging"'
                    ' panel, under "Tags".'))
    known_instructors = ManyToManyField(
        Person,
        _('Known instructors'),
        help_text=_('Instructors that match known people.'),
        editable=False,
        blank=True,
        null=True)
    assistants = TagAutocompleteField(
        _('Assistants'),
        help_text=_('Autocompleting, comma separated list of assistants.'
                    ' If typed nicely, the system will be able to'
                    ' automagically figure out known people. The complete'
                    ' list of assistants can be found into the "Tagging"'
                    ' panel, under "Tags".'),
        blank=True,
        null=True)
    known_assistants = ManyToManyField(
        Person,
        _('Known assistants'),
        help_text=_('Assistants that match known people.'),
        editable=False,
        blank=True,
        null=True)
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True)
    active = models.BooleanField(
        _('Active?'),
        default=True)
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
    link = models.URLField(
        _('Link'),
        blank=True,
        null=True)

    def __unicode__(self):
        return u'%s - %s (%s)' % (
            self.title,
            self.code,
            self.instructor)

def update_course(sender, instance, created, kwargs**):
    for i in ('instructors', 'assistants'):
        instance.known_instructors.add(
            list(set(getattr(instance, i).split(' ')) -
                 set([x.name for x in getattr(instance, 'known_%s' % i)]))*)
    instance.save()
signals.post_save.connect(update_course, sender=Course)


class Thesis(models.Model):
    """
    A thesis or a project to be assigned to a student.
    """
    class Meta:
        verbose_name = _('Thesis or project')
        verbose_name_plural = _('Theses or projects')

    title = models.CharField(
        _('Title'),
        max_length=256)
    published = models.BooleanField(
        _('Published?'),
        default=True)
    project = models.BooleanField(
        _('Can be a small project?'),
        default=False)
    students = models.ManyToManyField(
        Person,
        verbose_name=_('Assigned to'),
        related_name='theses',
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
        _('Description'))
    status = models.TextField(
        _('Status'),
        blank=True,
        null=True)
    topics = models.ManyToManyField(
        Topic,
        verbose_name=_('Research topics'))
    projects = models.ManyToManyField(
        Project,
        verbose_name=_('Research projects'),
        blank=True,
        null=True)
    advisors = models.ManyToManyField(
        Person,
        related_name='theses_advised',
        verbose_name=_('Advisors'))
    difficulty = models.PositiveSmallIntegerField(
        _('Expected Difficulty'),
        choices=config.DIFFICULTIES)
    downloads = models.ManyToManyField(
        Asset,
        verbose_name=_('Downloads'),
        blank=True,
        null=True)
    link = models.URLField(
        _('Link'),
        blank=True,
        null=True)
    skills = models.CharField(
        _('Required Skill'),
        max_length=256,
        blank=True,
        null=True)
    related_theses = models.ManyToManyField(
        'self',
        verbose_name=_('Related Theses'),
        blank=True,
        null=True)
    papers = models.ManyToManyField(
        Paper,
        verbose_name=_('Papers published'),
        blank=True)

    def __unicode__(self):
        return u'%s' % self.title

    def _assigned(self):
        return self.date_assigned is not None
    assigned = property(_assigned)

    def _completed(self):
        return self.date_completed is not None
    completed = property(_completed)


