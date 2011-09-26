from django.conf import settings

PEOPLE_DEFAULT_DIRECTORY = getattr(
    settings,
    'ACADEMIC_PEOPLE_DEFAULT_DIRECTORY',
    'people')

PEOPLE_DEFAULT_PICTURE = PEOPLE_DEFAULT_DIRECTORY + '/' + getattr(
    settings,
    'ACADEMIC_PEOPLE_DEFAULT_PICTURE',
    'default.jpg')

SPONSORS_DEFAULT_DIRECTORY = getattr(
    settings,
    'ACADEMIC_SPONSORS_DEFAULT_DIRECTORY',
    'sponsors')

DOWNLOADS_DEFAULT_DIRECTORY = getattr(
    settings,
    'ACADEMIC_DOWNLOADS_DEFAULT_DIRECTORY',
    'downloads')

PUBLISHING_DEFAULT_DIRECTORY = getattr(
    settings,
    'ACADEMIC_PUBLISHING_DEFAULT_DIRECTORY',
    'publishing')

TINYMCE_MCE_JS = getattr(
    settings,
    'ACADEMIC_TINYMCE_JS',
    None)

TINYMCE_SETUP_JS = getattr(
    settings,
    'ACADEMIC_TINYMCE_SETUP_JS',
    None)
