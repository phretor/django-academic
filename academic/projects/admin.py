from django.contrib import admin
from django import forms
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from academic.projects.models import *

class ProjectAdmin(admin.ModelAdmin):
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.STATIC_URL + 'academic/js/tiny_mce//tinymce_setup.js',
            )
    prepopulated_fields = {
	'slug': ('short_title',)
    }
    fieldsets = (
        (None, {
                'fields': (
                    'short_title',
		    'slug',
                    'title',
                    'excerpt',
                    'topic',
                    'description',
                    'people',
                    'publications'),}),
        (_('Extra information'), {
                'classes': (
                    'collapse closed collapse-closed',),
                'fields': (
                    'related_topics',
                    'redirect_to',
                    'downloads',
                    'organizations',
                    'sponsors',
                    'footer'),})
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
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.STATIC_URL + 'academic/js/tiny_mce//tinymce_setup.js',
            )
    prepopulated_fields = {
	'slug': ('title',)
    }
    list_display_links = [
        'title']
    list_display = [
        'title',
        'highlight',
        'highlight_order',
        'description']
admin.site.register(Topic, TopicAdmin)
