from django.contrib import admin
from gda.models import Token


class TokenAdmin(admin.ModelAdmin):
    search_fields = ('student', 'discipline')
    ordering = ['student']
    readonly_fields = ('token', 'used', 'discipline', 'student')

admin.site.register(Token, TokenAdmin)
