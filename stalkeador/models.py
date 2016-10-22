from django.db import models
from gda.tools.tokenGenerator import generateToken


class Token(models.Model):
    '''
        This is a model for a token to guarantee the anonymity of the Student
        and generates a link using this token
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
