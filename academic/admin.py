from django.contrib import admin
from django import forms
from django.db import models
from django.conf import settings

from academic.models import *

admin.site.register(Download)

class ProjectAdmin(admin.ModelAdmin):
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'behavior/tinymce_setup.js',
            )
    
    filter_horizontal = [
        'downloads',
        'people',
        'related_topics',
        'organizations',
        'sponsors',
        'publications']
    list_display_links = [
        'title']
    list_display = [
        'title',
        'short_title',
        'excerpt',
        'topic']
admin.site.register(Project, ProjectAdmin)

class TopicAdmin(admin.ModelAdmin):
    list_display_links = [
        'title']
    list_display = [
        'title',
        'highlight',
        'highlight_order',
        'description']
admin.site.register(Topic, TopicAdmin)
