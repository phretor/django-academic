from django.conf import settings

from django.utils.translation import ugettext as _

COLLABORATION_DIFFICULTIES = getattr(settings, 'ACADEMIC_COLLABORATION_DIFFICULTIES', (
    (1, _('Easy')),
    (2, _('Reasonable')),
    (3, _('Challenging')),
    (4, _('Difficult')),
    (5, _('You will have a paper on this!')),
))

COLLABORATION_TYPES = getattr(settings, 'ACADEMIC_COLLABORATION_TYPES', (
    (0, _('Project')),
    (1, _('Thesis')),
    (2, _('PhD Thesis')),
    (3, _('Job')),
))
