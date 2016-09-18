from django.contrib import admin
from gda.models import Questionnaire, Question, Choice, Answer


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
    list_display = ("question",)
    search_fields = ('offering__subject__code',
                     'question__id')
    ordering = ['question']

admin.site.register(Answer, AnswerAdmin)
