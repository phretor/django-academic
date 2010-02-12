from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext as _

from academic.models import *
from academic.forms import *

    
class RankAdmin(admin.ModelAdmin):
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'behavior/tinymce_setup.js',
        )

    list_display = (
        'name',
        'plural_name', )


class PersonAdmin(admin.ModelAdmin):
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'behavior/tinymce_setup.js',
        )

    list_display = (
        'first_name',
        'last_name',
        'e_mail',
        'web_page',)
    list_filter = (
        'public',)
    search_fields = (
        'first_name',
        'last_name',
        'e_mail',)


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'title', )
    list_filter = (
        'public',
        'date_starts',
        'date_ends',)
    search_fields = (
        'title',
        'code',)
    

class CollaborationAdmin(admin.ModelAdmin):
    form = CollaborationAdminForm
    list_display = (
        'title',
        'assigned',
        'completed',
        'type',
        'difficulty',
        'date_updated')
    list_filter = (
        'type',
        'public',
        'date_assigned',
        'date_completed',
        'date_published',
        'difficulty',)
    search_fields = (
        'topics',
        'title',
        'description')

    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'behavior/tinymce_setup.js',
        )

    
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = (
        'name',
        'description',)
    
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'behavior/tinymce_setup.js',
        )
    

class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'short_description',)
    list_display_links = (
        'name', )
    list_filter = (
        'public',
        'date_starts',
        'date_ends',
        'date_published',)
    search_fields = (
        'title',
        'short_description',
        'description',
        'people',)
    
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'behavior/tinymce_setup.js',
        )

    
class PaperTypeAdmin(admin.ModelAdmin):
    list_display  = (
        'name', )
    


class PaperAdmin(admin.ModelAdmin):
    form = PaperAdminForm
    list_display = (
        'title',
        'type',
        'year',)
    list_filter = (
        'year',
        'date_updated', )
    search_fields = (
        'title',
        'abstract',
        'authors',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(PaperType, PaperTypeAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Rank, RankAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Collaboration, CollaborationAdmin)
