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
    search_fields = ('subject', 'year', "semester")
    ordering = ['subject']

admin.site.register(Offering, OfferingAdmin)


class TeacherAdmin(admin.ModelAdmin):
    search_fields = ('name', 'id')
    ordering = ['name']

admin.site.register(Teacher, TeacherAdmin)


class InstituteAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name')
    ordering = ['code']

admin.site.register(Institute, InstituteAdmin)
