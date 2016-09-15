from django.contrib import admin
from gda.models import Token, Questionnaire, Question, Choice, Answer


class TokenAdmin(admin.ModelAdmin):
    search_fields = ('student', 'discipline')
    ordering = ['student']
    readonly_fields = ('token', 'used', 'discipline', 'student')

admin.site.register(Token, TokenAdmin)


class QuestionnaireAdmin(admin.ModelAdmin):
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
    search_fields = ('offering','question')
    ordering = ['question']

admin.site.register(Answer, AnswerAdmin)
