from django.conf import settings

PEOPLE_DEFAULT_PICTURE = getattr(
    settings,
    'ACADEMIC_PEOPLE_DEFAULT_PICTURE',
    None)

TINYMCE_MCE_JS = getattr(
    settings,
    'ACADEMIC_TINYMCE_JS',
    settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js')

TINYMCE_SETUP_JS = getattr(
    settings,
    'ACADEMIC_TINYMCE_SETUP_JS',
    settings.STATIC_URL + 'academic/js/tiny_mce//tinymce_setup.js')
