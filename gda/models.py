from django.db import models
from dacParser.models import Student, Offering
from gda.tools.tokenGenerator import generateToken


class Token(models.Model):
    student = models.ForeignKey(Student)
    token = models.CharField(max_length = 37,
                             default=generateToken(student.name),
                             primary_key=True)
    discipline = models.ForeignKey(Offering)
    used = models.BooleanField(default = False)

    class Meta:
        unique_together = ["student", "discipline", "token"]

    def __str__(self):
        # return self.token
        return (str(self.student)+' - '+str(self.discipline.code)+' - ' +
                str(self.token))


class Questionnaire(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        # return self.token
        return str(self.name)



class Question(models.Model):
    text = models.TextField()

    type = models.CharField(
             choices = (("text","text"),
                        ("option","option"),
                        ("numeric","numeric")),
             max_length = 15)

    choices = models.ManyToManyField(Choice)


class Choice(models.Model):
    text = models.TextField()

class Answer(models.Model):
    text = models.TextField()
    offering = models.ManyToManyField(Offering)
    Question = models.ForeignKey(Question)




