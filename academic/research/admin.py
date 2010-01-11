from django.contrib import admin
from research.models import *

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = (
        'name',
        'description',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'published',
        'name',
        'short_description',)
    list_display_links = (
        'name', )
    list_filter = (
        'published',
        'date_starts',
        'date_ends',
        'date_published',)
    search_fields = (
        'title',
        'short_description',
        'description',
        'people',)

class PaperTypeAdmin(admin.ModelAdmin):
    list_display  = ('name', )

class PaperAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'authors',
        'type',
        'year',)
    list_filter = (
        'year',
        'date_updated', )
    search_fields = (
        'title',
        'abstract',
        'authors',)

admin.site.register(Topic, TopicAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(PaperType, PaperTypeAdmin)
admin.site.register(Paper, PaperAdmin)
