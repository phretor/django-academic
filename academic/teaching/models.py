from django.db import models
from django.utils.translation import ugettext as _

from people.models import *
from research.models import *
from assets.models import *
from teaching import config


class Course(models.Model):
    """
    A course such as Math I, Advanced Topics in Information Security.
    """
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        
    title = models.CharField(
        _('Title'),
        max_length=256)
    code = models.CharField(
        _('Code'),
        max_length=16)
    instructor = models.ForeignKey(
        Person,
        verbose_name=_('Instructor'),
        related_name='courses_as_instructor')
    assistants = models.ManyToManyField(
        Person,
        verbose_name=_('Teaching Assistants'),
        blank=True,
        null=True,
        related_name='courses_as_assistant')
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
        return u'%s - %s (%s)' % (self.title, self.code, self.instructor)


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
