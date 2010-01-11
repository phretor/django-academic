from django.contrib import admin

from teaching.models import *

class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'title',
        'instructor')
    list_filter = (
        'active',
        'published',
        'published',
        'date_starts',
        'date_ends',)
    search_fields = (
        'title',
        'code',
        'instructor',)
admin.site.register(Course, CourseAdmin)

class ThesisAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'assigned',
        'completed',
        'project',
        'difficulty',
        'date_updated')
    list_filter = (
        'project',
        'published',
        'date_assigned',
        'date_completed',
        'date_published',
        'difficulty',)
    search_fields = (
        'topics',
        'title',
        'description')
admin.site.register(Thesis, ThesisAdmin)
