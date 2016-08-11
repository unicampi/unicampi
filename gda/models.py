from django.db import models
from dacParser.models import Student, Class
from gda.tools.tokenGenerator import generateToken

# Create your models here.

class Token(models.Model):
    student = models.ForeignKey(Student)
    discipline = models.ForeignKey(Class)
    token = models.CharField(max_length = 37, default = generateToken())
    used = models.BooleanField(default = False)

    class Meta:
        unique_together = ["student"]

    def __str__(self):
        return str(self.student)+' - '+str(self.discipline.code)
