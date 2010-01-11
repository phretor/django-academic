from django.contrib import admin

from people.models import *

class RankAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'plural_name', )


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'e_mail',
        'web_page',)
    list_filter = (
        'active',
        'published',)
    search_fields = (
        'first_name',
        'last_name',
        'e_mail',)

    
admin.site.register(Rank, RankAdmin)
admin.site.register(Person, PersonAdmin)
