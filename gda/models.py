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
    REFERENCE_TYPES = (
        ('T', 'Teacher'),
        ('O', 'Offering'),
        ('S', 'Subject'),
    )

    text = models.TextField()
    helper = models.TextField(blank=True,
                              help_text="Texto auxiliar para questão. Ex: 'Valores entre 10 e 20'"
                              )
    ref = models.CharField(choices = REFERENCE_TYPES,
                            max_length = 2,
                            help_text="Essa questão referencia a quem?"
                            )
    typ = models.CharField(choices = QUESTION_TYPES,
                            max_length = 2,
                            help_text="O tipo da questão?"
                            )
    choices = models.ManyToManyField('Choice',
                                      blank=True,
                                      help_text="Possiveis alternativas para questões Option"
                                      )
    min_v = models.IntegerField(default=0,blank=True,help_text="Menor valor possivel")
    max_v = models.IntegerField(default=0,blank=True,help_text="Maior valor possivel")

    def __str__(self):
        return str(self.pk) + ' - ' + self.text[:50]


class Choice(models.Model):
    text = models.TextField(help_text="Texto da alternativa")

    def __str__(self):
        return str(self.text)

class Answer(models.Model):
    text = models.TextField()
    choice = models.ForeignKey('Choice',
                                null=True,
                                blank=True
                                )
    question = models.ForeignKey('Question')
