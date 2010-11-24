from django.contrib import admin
from django import forms
from django.db import models
from django.conf import settings

from academic.people.models import *

class PersonAdmin(admin.ModelAdmin):
    filter_horizontal = [
        'affiliation',]
    list_display_links = (
        'name',)
    list_display = (
        'name',
        'has_picture',
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
