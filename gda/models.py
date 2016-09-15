from django.db import models
from gda.tools.tokenGenerator import generateToken


class Token(models.Model):
    student = models.ForeignKey('dacParser.Student')
    token = models.CharField(primary_key=True,
                             max_length = 37,
                             default=generateToken(student.name),
                             editable=False,
                             )
    discipline = models.ForeignKey('dacParser.Offering')
    used = models.BooleanField(default = False)

    class Meta:
        unique_together = ["student", "discipline", "token"]

    def __str__(self):
        # return self.token
        return (str(self.student)+' - '+str(self.discipline.code)+' - ' +
                str(self.token))


class Questionnaire(models.Model):
    name = models.CharField(max_length = 50)
    questions = models.ManyToManyField('Question', blank=True)

    def __str__(self):
        return str(self.pk) + ' - ' + self.name



class Question(models.Model):
    QUESTION_TYPES = (
        ('T','Text'),
        ('O', 'Option'),
        ('N','Numeric'),
    )

    text = models.TextField()
    type = models.CharField(choices = QUESTION_TYPES,
                            max_length = 2,
                            )
    choices = models.ManyToManyField('Choice',
                                      blank=True
                                     )
    def __str__(self):
        return str(self.pk) + ' - ' + self.text[:50]


class Choice(models.Model):
    text = models.TextField()

class Answer(models.Model):
    text = models.TextField()
    offering = models.ForeignKey('dacParser.Offering')
    question = models.ForeignKey(Question)
