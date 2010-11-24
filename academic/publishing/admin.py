from django.contrib import admin
from django import forms
from django.db import models
from django.conf import settings
from django.core import validators

from academic.publishing.models import *

class ConferenceEditionAdmin(admin.ModelAdmin):
    list_display_links = (
        'nickname',)
    list_display = (
        'nickname',
        'month',
        'year',
        'address',
        'web_page')
admin.site.register(ConferenceEdition, ConferenceEditionAdmin)

class ConferenceEditionInlineForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = (
            'year',
            'month',
            'address',)

class ConferenceEditionInline(admin.TabularInline):
    model = ConferenceEdition
    form = ConferenceEditionInlineForm

class ConferenceAdmin(admin.ModelAdmin):
    inlines = [
        ConferenceEditionInline, ]
    list_display = (
        'name',
        'acronym', )
admin.site.register(Conference, ConferenceAdmin)

class ConferenceProceedingsAdmin(admin.ModelAdmin):
    list_display_links = (
        'title',)
    list_display = (
        'title',
        'year',
        'volume',
        'number',
        'edition')
admin.site.register(ConferenceProceedings, ConferenceProceedingsAdmin)

class AuthorshipInline(admin.TabularInline):
    verbose_name = 'Author'
    verbose_name_plural = 'Authors'
    model = Authorship
    extra = 5

class PublicationAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'nickname': ('title',)
        }
    inlines = (AuthorshipInline,)
    list_display_links = (
        'nickname',)
    list_display = (
        'nickname',
        'title',
        'year',)

admin.site.register(ConferenceArticle, PublicationAdmin)
admin.site.register(JournalArticle, PublicationAdmin)
admin.site.register(TechnicalReport, PublicationAdmin)

class AdvisorshipInline(admin.TabularInline):
    verbose_name = 'Advisor'
    verbose_name_plural = 'Advisors'
    model = Advisorship
    extra = 1

class CoadvisorshipInline(admin.TabularInline):
    verbose_name = 'Coadvisor'
    verbose_name_plural = 'Coadvisors'
    model = Coadvisorship
    extra = 1

class ThesisAdmin(PublicationAdmin):
    inlines = (
        AdvisorshipInline,
        CoadvisorshipInline)

class ReviewingInline(admin.TabularInline):
    verbose_name = 'Reviewer'
    verbose_name_plural = 'Reviewers'
    model = Reviewing
    extra = 1

class PhdThesisAdmin(ThesisAdmin):
    inlines = (
        AdvisorshipInline,
        CoadvisorshipInline,
        ReviewingInline)

admin.site.register(MasterThesis, ThesisAdmin)
admin.site.register(PhdThesis, PhdThesisAdmin)

class EditorshipInline(admin.TabularInline):
    verbose_name = 'Editor'
    verbose_name_plural = 'Editors'
    model = Editorship
    extra = 5

class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'nickname': ('title',)
        }
    inlines = (EditorshipInline,)
    list_display_links = (
        'title',)
    list_display = (
        'title',
        'year',
        'volume',
        'number',
        'edition')
admin.site.register(Book, BookAdmin)
admin.site.register(Journal, BookAdmin)
admin.site.register(BookChapter, BookAdmin)
