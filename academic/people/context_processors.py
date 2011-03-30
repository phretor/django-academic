from academic import settings

def default_picture_url(context):
    return {
        'ACADEMIC_PEOPLE_DEFAULT_PICTURE':
            settings.PEOPLE_DEFAULT_PICTURE, }
