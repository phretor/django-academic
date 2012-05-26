import posixpath

from django.conf import settings

PEOPLE_DEFAULT_DIRECTORY = getattr(
    settings,
    'ACADEMIC_PEOPLE_DEFAULT_DIRECTORY',
    'people')

PEOPLE_DEFAULT_PICTURE = posixpath.join(PEOPLE_DEFAULT_DIRECTORY, getattr(
    settings,
    'ACADEMIC_PEOPLE_DEFAULT_PICTURE',
    'default.jpg'))
