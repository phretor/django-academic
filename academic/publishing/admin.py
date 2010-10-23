from django.contrib import admin
from django import forms
from django.db import models
from django.conf import settings

from academic.publications.models import *

class ConferenceEditionAdmin(admin.ModelAdmin):
    list_display_links = (
        'conference',)
    list_display = (
        'conference',
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
    exclude = (
        'authors',)
    list_display_links = (
        'title',)
    list_display = (
        'title',
        'year',
        'volume',
        'number',
        'edition')
admin.site.register(ConferenceProceedings, ConferenceProceedingsAdmin)

class BookAdminModelForm(forms.ModelForm):
    class Meta:
        model = Book
    
    def clean(self):
        cleaned_data = self.cleaned_data
        authors = cleaned_data.get('authors')
        editors = cleaned_data.get('editors')

        if authors and editors:
            raise forms.ValidationError('BibTeX disallows having both'\
                                            ' authors and editors.')
        return cleaned_data

class BookAdmin(admin.ModelAdmin):
    form = BookAdminModelForm
    filter_horizontal = [
        'authors',
        'editors', ]
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

class PublicationAdmin(admin.ModelAdmin):
    filter_horizontal = ['authors', ]
    list_display_links = (
        'nickname',)
    list_display = (
        'nickname',
        'title',
        'year',)

admin.site.register(ConferenceArticle, PublicationAdmin)
admin.site.register(JournalArticle, PublicationAdmin)
admin.site.register(TechnicalReport, PublicationAdmin)
admin.site.register(MasterThesis, PublicationAdmin)
admin.site.register(PhdThesis, PublicationAdmin)
