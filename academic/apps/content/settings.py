from django.conf import settings

DOWNLOADS_DEFAULT_DIRECTORY = getattr(
    settings,
    'ACADEMIC_DOWNLOADS_DEFAULT_DIRECTORY',
    'downloads')
