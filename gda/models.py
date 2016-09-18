from django.db import models


class Questionnaire(models.Model):
    name = models.CharField(max_length = 50)
    questions = models.ManyToManyField('Question',
                                        blank=True
                                    )

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

    def __str__(self):
        return str(self.text)

class Answer(models.Model):
    text = models.TextField()
    choice = models.ForeignKey('Choice',
                                null=True,
                                blank=True
                                )
    question = models.ForeignKey('Question')
