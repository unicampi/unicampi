from django.contrib import admin
from dacParser.models import Student, Discipline, Teacher

# This is the layout for students on admin page - this generates the search
class StudentAdmin(admin.ModelAdmin):
    search_fields = ('name', 'ra', )
    ordering = ['ra']

admin.site.register(Student, StudentAdmin)


class DisciplineAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code', "classes")
    ordering = ['code']

admin.site.register(Discipline, DisciplineAdmin)

class TeacherAdmin(admin.ModelAdmin):
    search_fields = ('name', 'id')
    ordering = ['name']

admin.site.register(Teacher, TeacherAdmin)
