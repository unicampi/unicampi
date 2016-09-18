from django.contrib import admin
from stalkeador.models import Token

class TokenAdmin(admin.ModelAdmin):
    # To make it easy to order
    list_display = ("offering", "student")
    fields = ('offering', 'student', 'used')
    search_fields = ('token','student__name','student__ra', 'offering__subject__code')
    ordering = ['student']
    readonly_fields = ('token', 'used', 'offering', 'student')


admin.site.register(Token, TokenAdmin)
