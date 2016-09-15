from django.contrib import admin
from gda.models import Token, Questionnaire, Question, Choice, Answer


class TokenAdmin(admin.ModelAdmin):
    # To make it easy to order
    list_display = ("offering", "student")
    fields = ('offering', 'student', 'used')
    search_fields = ('student__name','student__ra', 'offering__subject__code')
    ordering = ['student']
    readonly_fields = ('token', 'used', 'offering', 'student')


admin.site.register(Token, TokenAdmin)


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    search_fields = ('id','name')
    ordering = ['id']

admin.site.register(Questionnaire, QuestionnaireAdmin)


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('text','type')
    ordering = ['id']

admin.site.register(Question, QuestionAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    search_fields = ('id','text')
    ordering = ['id']

admin.site.register(Choice, ChoiceAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "offering")
    search_fields = ('offering__subject__code',
                     'question__id')
    ordering = ['question']

admin.site.register(Answer, AnswerAdmin)
