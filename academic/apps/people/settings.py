from django.conf import settings
import os

PEOPLE_DEFAULT_DIRECTORY = getattr(
    settings,
    'ACADEMIC_PEOPLE_DEFAULT_DIRECTORY',
    'people')

PEOPLE_DEFAULT_PICTURE = os.path.join(
        PEOPLE_DEFAULT_DIRECTORY, getattr(
            settings,
            'ACADEMIC_PEOPLE_DEFAULT_PICTURE',
            'default.jpg')
        )
