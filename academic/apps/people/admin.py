from django.contrib import admin
from django import forms
from django.db import models
from django.conf import settings

from academic.people.models import *

class PersonAdmin(admin.ModelAdmin):
    filter_horizontal = [
        'affiliation',]
    list_display_links = (
        'photo',
        'first_name',
        'last_name')
    list_display = (
        'photo',
        'first_name',
        'last_name',
        'rank',
        'public',
        'current',
        'alumni',
        'visitor',
        'e_mail',
        'web_page',)
    list_editable = (
        'rank',
        'public',
        'current',
        'alumni',
        'visitor',
        'e_mail',
        'web_page')
    list_filter = (
        'public',
        'current',
        'visitor',
        'alumni')
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
