from django.db import models
from dacParser.models import Student, Class
from gda.tools.tokenGenerator import generateToken


class Token(models.Model):
    student = models.ForeignKey(Student)
    token = models.CharField(max_length = 37,
                             default=generateToken(student.name),
                             unique=True)
    discipline = models.ForeignKey(Class)
    used = models.BooleanField(default = False)

    class Meta:
        unique_together = ["student", "discipline", "token"]

    def __str__(self):
        # return self.token
        return (str(self.student)+' - '+str(self.discipline.code)+' - ' +
                str(self.token))
