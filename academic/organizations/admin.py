from django.contrib import admin
from django import forms
from django.db import models
from django.conf import settings

from academic.organizations.models import *

class OrganizationAdmin(admin.ModelAdmin):
    list_display_links = (
        'acronym',)
    list_display = (
        'acronym',
        'name',
        'web_page',
        'country',)
    list_editables = (
        'acronym',
        'name',
        'web_page',
        'country',)
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
admin.site.register(Sponsor, SponsorAdmin)
