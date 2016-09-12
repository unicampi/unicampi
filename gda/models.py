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
