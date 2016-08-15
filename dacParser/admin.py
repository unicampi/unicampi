from django.contrib import admin
from dacParser.models import Student, Class, Course, Teacher, Institute


# This is the layout for students on admin page - this generates the search
class StudentAdmin(admin.ModelAdmin):
    search_fields = ('name', 'ra')
    ordering = ['ra']

admin.site.register(Student, StudentAdmin)


class CourseAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name', "type")
    ordering = ['code']

admin.site.register(Course, CourseAdmin)


class ClassAdmin(admin.ModelAdmin):
    search_fields = ('code', 'year', "semester")
    ordering = ['code']

admin.site.register(Class, ClassAdmin)


class TeacherAdmin(admin.ModelAdmin):
    search_fields = ('name', 'id')
    ordering = ['name']

admin.site.register(Teacher, TeacherAdmin)


class InstituteAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name')
    ordering = ['code']

admin.site.register(Institute, InstituteAdmin)
