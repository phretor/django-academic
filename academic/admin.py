from django.contrib import admin
from django import forms
from django.db import models
from django.conf import settings

from academic.models import *

class PersonAdmin(admin.ModelAdmin):
    filter_horizontal = [
        'affiliation',]
    list_display_links = (
        'name',)
    list_display = (
        'name',
        'public',
        'current',
        'first_name',
        'last_name',
        'e_mail',
        'web_page',
        'rank')
    list_editable = (
        'public',
        'current',
        'e_mail',
        'web_page',
        'rank')
    list_filter = (
        'public',)
    search_fields = (
        'first_name',
        'last_name',
        'e_mail',)
admin.site.register(Person, PersonAdmin)

class PersonInlineForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = (
            'public',
            'first_name',
            'last_name',
            'e_mail')

class PersonInline(admin.TabularInline):
    model = Person
    form = PersonInlineForm

class RankAdmin(admin.ModelAdmin):
    inlines = [
        PersonInline, ]
    list_display = (
        'name',
        'plural_name', )
admin.site.register(Rank, RankAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    list_display_links = (
        'acronym',)
    list_display = (
        'acronym',
        'name',
        'web_page',
        'country',)
    list_editable = (
        'name',
        'country',
        'web_page',)
    search_fields = (
        'name',
        'country',
        'acronym',)
admin.site.register(Institution, OrganizationAdmin)
admin.site.register(Publisher, OrganizationAdmin)
admin.site.register(School, OrganizationAdmin)

class SponsorAdmin(OrganizationAdmin):
    list_display = (
        'order',
        'acronym',
        'name',
        'web_page',
        'country',)
    list_editable = (
        'order',
        'name',
        'country',
        'web_page',)
admin.site.register(Sponsor, SponsorAdmin)


class ConferenceEditionAdmin(admin.ModelAdmin):
    list_display_links = (
        'conference',)
    list_display = (
        'conference',
        'month',
        'year',
        'address',
        'web_page')
    list_editable = (
        'year',
        'month',
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
    list_editable = (
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
    list_editable = (
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
    list_editable = (
        'title',
        'year')
admin.site.register(ConferenceArticle, PublicationAdmin)
admin.site.register(JournalArticle, PublicationAdmin)
admin.site.register(TechnicalReport, PublicationAdmin)
admin.site.register(MasterThesis, PublicationAdmin)
admin.site.register(PhdThesis, PublicationAdmin)

class ProjectAdmin(admin.ModelAdmin):
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'behavior/tinymce_setup.js',
            )
    
    filter_horizontal = [
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
    list_editable = [
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
    list_editable = [
        'highlight',
        'highlight_order']
admin.site.register(Topic, TopicAdmin)
