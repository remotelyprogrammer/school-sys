from django.contrib import admin
from .models import Enrollment, SchoolYear, GradeLevel, Subject

admin.site.register(Enrollment)
admin.site.register(GradeLevel)
admin.site.register(Subject)


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ('start_year', 'end_year', 'is_current')
    list_filter = ('is_current',)
    actions = ['make_current']

    def make_current(self, request, queryset):
        queryset.update(is_current=False)  # Clear current status of all
        queryset.first().is_current = True  # Set first selected as current
        queryset.first().save()
    make_current.short_description = "Mark selected school year as current"
