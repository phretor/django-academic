from django.conf import settings

from academic.apps.settings import *
from academic.settings.base import *

try:
    from local_settings import *
except ImportError:
    pass
