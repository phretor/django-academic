from django.conf import settings

LOGIN_FORM_CLASS = getattr(
    settings,
    'PROTAGS_LOGIN_FORM_CLASS',
    'django.contrib.auth.forms.AuthenticationForm')

PROTOCOL = getattr(
    settings,
    'PROTAGS_PROTOCOL',
    'http')

# must contain %(query)s
GMAPS_URL = getattr(
    settings,
    'PROTAGS_GMAPS_URL',
    'http://maps.google.com/maps?f=q&q=%(query)s')

SANITIZE_ALLOWED_TAGS = getattr(
    settings,
    'PROTAGS_SANITIZE_ALLOWED_TAGS',
    'strong em p ul ol li')
