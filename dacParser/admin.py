from django.contrib import admin
from dacParser.models import Student, Offering, Subject, Teacher, Institute


# This is the layout for students on admin page - this generates the search
class StudentAdmin(admin.ModelAdmin):
    search_fields = ('name', 'ra')
    ordering = ['ra']

admin.site.register(Student, StudentAdmin)


class SubjectAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name', "type")
    ordering = ['code']

admin.site.register(Subject, SubjectAdmin)


class OfferingAdmin(admin.ModelAdmin):
    # list_display = ("subject__code", "offering_id")
    readonly_fields = ('answers',)
    search_fields = ('subject__code', 'year', "semester")
    ordering = ['subject', 'offering_id', 'year', 'semester']

admin.site.register(Offering, OfferingAdmin)


class TeacherAdmin(admin.ModelAdmin):
    search_fields = ('name', 'id')
    ordering = ['name']

admin.site.register(Teacher, TeacherAdmin)


class InstituteAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name')
    ordering = ['code']

admin.site.register(Institute, InstituteAdmin)
