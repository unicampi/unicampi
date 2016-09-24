from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from gda.models import Questionnaire, Question, Choice, Answer

## Questionnaires
# Class to import and export Questionnaire
class QuestionnaireResource(resources.ModelResource):

    class Meta:
        model = Questionnaire

class QuestionnaireAdmin(ImportExportModelAdmin):
    resource_class = QuestionnaireResource
    list_display = ("pk", "name")
    search_fields = ('id','name')
    ordering = ['id']

admin.site.register(Questionnaire, QuestionnaireAdmin)


## Questions
# Class to import and export Questions
class QuestionResource(resources.ModelResource):

    class Meta:
        model = Question

class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    search_fields = ('text','type')
    ordering = ['id']

admin.site.register(Question, QuestionAdmin)


## Choices
class ChoiceResource(resources.ModelResource):

    class Meta:
        model = Choice

class ChoiceAdmin(ImportExportModelAdmin):
    resource_class = ChoiceResource
    search_fields = ('id','text')
    ordering = ['id']

admin.site.register(Choice, ChoiceAdmin)


## Answers
class AnswerResource(resources.ModelResource):

    class Meta:
        model = Answer

class AnswerAdmin(ImportExportModelAdmin):
    resource_class = AnswerResource
    list_display = ("question",)
    search_fields = ('offering__subject__code',
                     'question__id')
    ordering = ['question']

admin.site.register(Answer, AnswerAdmin)
