from django.db import models
from gda.tools.tokenGenerator import generateToken


class Token(models.Model):
    '''
        This is a model for a token to guarantee the anonymity of the Student
    '''
    student = models.ForeignKey('dacParser.Student')
    token = models.CharField(primary_key=True,
                             unique=True,
                             max_length = 37,
                             editable=False,
                             )
    offering = models.ForeignKey('dacParser.Offering')
    used = models.BooleanField(default = False)

    class Meta:
        unique_together = ["student", "offering"]

    def __str__(self):
        return (str(self.offering.subject.code) +' - '+
                 str(self.student))

    # This function is to autogenerate the token when saving the model to de db
    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = generateToken(self.student.name + str(self.offering))
        super().save(*args, **kwargs)


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

class Answer(models.Model):
    text = models.TextField()
    offering = models.ForeignKey('dacParser.Offering')
    question = models.ForeignKey(Question)
