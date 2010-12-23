from django.conf import settings

try:
	static_url = settings.STATIC_URL
except:
	static_url = settings.MEDIA_URL

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
    static_url + 'academic/js/tiny_mce//tinymce_setup.js')
