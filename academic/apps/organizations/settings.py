from django.conf import settings

SPONSORS_DEFAULT_DIRECTORY = getattr(
    settings,
    'ACADEMIC_SPONSORS_DEFAULT_DIRECTORY',
    'sponsors')
