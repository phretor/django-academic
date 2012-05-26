from django.conf import settings

PUBLISHING_DEFAULT_DIRECTORY = getattr(
    settings,
    'ACADEMIC_PUBLISHING_DEFAULT_DIRECTORY',
    'publishing')
