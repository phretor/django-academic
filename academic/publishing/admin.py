from django.contrib import admin
from django import forms
from django.db import models
from django.conf import settings
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from academic.publishing.models import *

class ConferenceEditionAdmin(admin.ModelAdmin):
    actions = ('prepare_proceedings',)
    def prepare_proceedings(self, request, queryset):
        c, e = 0, 0
        for ce in queryset:
            title = ce.conference.name
            year = ce.year
            cp = ConferenceProceedings(
                conference_edition=ce,
                title=title,
                year=year)
            if ce.month != '':
                cp.month = ce.month
            cp.save()
        
    list_display_links = (
        'conference',)
    list_display = (
        'conference',
        'year',
        'address',
        'web_page')
admin.site.register(ConferenceEdition, ConferenceEditionAdmin)

class ConferenceEditionInlineForm(forms.ModelForm):
    class Meta:
        model = ConferenceEdition
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

class AuthorshipInline(admin.TabularInline):
    verbose_name = 'Author'
    verbose_name_plural = 'Authors'
    model = Authorship
    extra = 5

class PublicationAdmin(admin.ModelAdmin):
    inlines = (AuthorshipInline,)
    list_display_links = (
        'title',)
    list_display = (
        'author_list',
        'title',
        'year',)

admin.site.register(TechnicalReport, PublicationAdmin)

class PaperAdmin(PublicationAdmin):
    class Media:
        css = {
            'screen': (
                'academic/admin/js/inline_author_helper.css',) }
        js = (
            'academic/admin/js/inline_author_helper.js', )
    pass

class ConferenceArticleAdmin(PaperAdmin):
    fieldsets = (
        (None, {
                'fields': (
                    'crossref',
                    'title',
                    'year',
                    'month',
                    'fulltext',
                    'abstract',
                    'bibtex')
                }),
        (_('Extra information'), {
                'fields': (
                    'attachment',
                    'notes',)}),
        )
    list_display = (
        'author_list',
        'title',
        'year',)

class JournalArticleAdmin(PaperAdmin):
    fieldsets = (
        (None, {
                'fields': (
                    'journal',
                    'title',
                    'year',
                    'month',
                    'fulltext',
                    'abstract',
                    'bibtex')
                }),
        (_('Extra information'), {
                'fields': (
                    'attachment',
                    'notes',)}),
        )
    list_display = (
        'author_list',
        'title',
        'year',
        'journal')
    
admin.site.register(ConferenceArticle, ConferenceArticleAdmin)
admin.site.register(JournalArticle, JournalArticleAdmin)

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

class BookAdmin(PublicationAdmin):
    inlines = (
        AuthorshipInline,
        EditorshipInline,)
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

class ConferenceProceedingsAdmin(BookAdmin):
    fieldsets = (
        (None, {
                'fields': (
                    'conference_edition',
                    'title',
                    'year',
                    'month',
                    'number',
                    'volume',
                    'publisher',)
                }),
        (_('Extra information'), {
                'classes': (
                    'collapse closed collapse-closed',),
                'fields': (
                    'attachment',
                    'fulltext',
                    'address',
                    'edition',
                    'notes',)}),
        )
    inlines = (
        EditorshipInline,)
    list_display_links = (
        'title',)
    list_display = (
        'title',
        'conference_edition',
        'volume',
        'number')
admin.site.register(ConferenceProceedings, ConferenceProceedingsAdmin)
