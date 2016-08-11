from django.db import models
from dacParser.models import Student, Class

# Create your models here.

class Tokens(models.Model):
    student = models.ForeignKey(Student)
    discipline = models.ForeignKey(Class)
    token = models.CharField(max_length=100)
    used = models.BooleanField(default=False)

    class Meta:
        unique_together = ["student"]

    def __str__(self):
        return str(self.student)+' - '+str(self.discipline.code)
