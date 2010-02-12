from django.forms import *
from django.utils.translation import ugettext as _
from django.conf import settings
from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete

from academic.models import *

from ajax_filtered_fields.forms import AjaxManyToManyField

class PaperAdminForm(ModelForm):
    class Meta:
        model = Paper
    
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'js/SelectBox.js',
            settings.ADMIN_MEDIA_PREFIX + 'js/SelectFilter2.js',
            settings.MEDIA_URL + 'ajax_filtered_fields/js/ajax_filtered_fields.js',
        )

    topics = AjaxManyToManyField(
        Topic,
        ( ('All', {}), ),
        required=False )
    
    projects = AjaxManyToManyField(
        Project,
        ( ('All', {}), ),
        required=False )

    

class CollaborationAdminForm(ModelForm):
    assigned_to = AjaxManyToManyField(
        Person,
        ( ('All', {}), ),
        required=False )

    related_collaborations = AjaxManyToManyField(
        Collaboration,
        ( ('All', {}), ),
        required=False )

    published_papers = AjaxManyToManyField(
        Paper,
        ( ('All', {}), ),
        required=False )

    supervisors = AjaxManyToManyField(
        Person,
        ( ('All', {}), ) )
    
    topics = AjaxManyToManyField(
        Topic,
        ( ('All', {}), ) )
    
    related_projects = AjaxManyToManyField(
        Project,
        ( ('All', {}), ),
        required=False)

    class Meta:
        models = Collaboration
        
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'js/SelectBox.js',
            settings.ADMIN_MEDIA_PREFIX + 'js/SelectFilter2.js',
            settings.MEDIA_URL + 'ajax_filtered_fields/js/ajax_filtered_fields.js',
        )
