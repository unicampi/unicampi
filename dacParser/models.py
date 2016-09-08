from django.db import models
import uuid                   # To generate tokens
from unidecode import unidecode


# We should discuss all the models

class Student(models.Model):
    """
    Modelo de um aluno da unicamp
    school é o número do curso da unicamp
    course_type é p tipo do curso - nao se aplica a todos
    """
    ra = models.CharField(max_length=7, unique=True)
    name = models.CharField(max_length=150)
    school = models.CharField(max_length=15)
    course_type = models.CharField(max_length=4)
    disciplines = models.ManyToManyField('Class')

    def __str__(self):
        return (str(self.ra) + ' - ' + self.name)

    # This method returns a string containing the path to the object
    def url(self):
        return ('/s/' + str(self.ra))

    def AcademicEmail(self):
        firstLetter = self.name[0].lower()
        firstLetter = unidecode(firstLetter)
        ra = str(self.ra)
        mail = '@dac.unicamp.br'
        return (firstLetter + ra + mail)

    # This is to avoid having two or more equal students, they are the same if
    # the name RA and School is the same
    class Meta:
        unique_together = ["name", "ra", "school"]


class Course(models.Model):
    """
    Detalhes sobre uma disciplina. Cada disciplina possui um questionário
    associado.
    """

    COURSE_TYPE = [
        ('U', 'Undergraduate'),
        ('G', 'Graduate'),
    ]
    code = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=1, choices=COURSE_TYPE)
    classes = models.ManyToManyField('Class')
    descryption = models.CharField(max_length=1024)

    class Meta:
        unique_together = ('code', 'name', 'type')

    def __str__(self):
        return self.code + ' - ' + self.name

    # This method returns a string containing the path to the object
    def url(self):
        return '/d/'+self.code


class Class(models.Model):
    """
    Detalhes sobre cada turma de uma disciplina, as respostas aos questionários
    ficam associadas à turma.
    """

    code = models.CharField(max_length=6)   #duplicated but im logically inbcpb
    class_id = models.CharField(max_length=2)
    semester = models.CharField(max_length=2)
    year = models.CharField(max_length=5)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    vacancies = models.IntegerField()
    registered = models.IntegerField()
    students = models.ManyToManyField(Student)

    class Meta:
        unique_together = (("code","class_id", "year", "semester"),)

    def __str__(self):
        return self.code+'-'+self.class_id+' '+self.semester+'s'+self.year

    # This method returns a string containing the path to the object
    def url(self):
        return '/d/'+self.code+'/'+self.year+'/'+self.semester+'/'+self.class_id


# This object stores the teacher
class Teacher(models.Model):
    """
    Modelo de um professor

    """
    name = models.CharField(max_length=150)
    mail = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def url(self):
        return('/t/' + str(self.name))


# This is an object for a course
# eache course has an year and each year has a curriculun
#class Course(models.Model):
#    name = models.CharField(max_length=150)
#    code = models.IntegerField()
#    year = models.CharField(max_length=10)
#    # Podemos colocar catalogos


class Institute(models.Model):
    """
    Modelo de um instituto da unicamp
    """
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.code + ' - ' + self.name
