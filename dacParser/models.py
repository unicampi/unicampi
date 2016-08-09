from django.db import models
import uuid                   # To generate tokens


# We should discuss all the models
# This object stores student
class Student(models.Model):
    ra = models.CharField(max_length=7)
    name = models.CharField(max_length=150)
    course = models.IntegerField()
    course_type = models.CharField(max_length=10)
    disciplines = models.ManyToManyField('Discipline')

    def __str__(self):
        return (str(self.ra) + ' - ' + self.name)

    # This method returns a string containing the path to the object
    def url(self):
        return ('/s/' + str(self.ra))

    def AcademicEmail(self):
        firstLetter = self.name[0].lower()
        ra = str(self.ra)
        mail = '@dac.unicamp.br'
        return (firstLetter + ra + mail)

    # This is to avoid having two or more equal students, they are the same if
    # the name and RA are the same
    class Meta:
        unique_together = ["name", "ra"]


# This is the object thar stores subjects
class Discipline(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=150)
    year = models.CharField(max_length=5)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    classes = models.CharField(max_length=150)
    students = models.ManyToManyField(Student)
    semester = models.CharField(max_length=2)
    vacancies = models.IntegerField()
    registered = models.IntegerField()

    # To help on debug and kind of pretty
    def __str__(self):
        return (self.code + ' ' + self.classes + ' - ' + self.name)

    # This method returns a string containing the path to the object
    def url(self):
        return '/d/'+self.code+'/'+self.year+'/'+self.semester+'/'+self.classes

    # This function returns tokens for each student in the discipline like :
    # [(Student, token), (...),]
    def generateTokens(self):
        list = []
        for student in students.all():
            list.append((student,str(uuid.uuid4())))
    # This is to avoid having two or more equal students, they are the same if
    # the name and RA are the same
    class Meta:
        unique_together = ["name", "code", "classes", "year", "semester",
                            "teacher"]


# This object stores the teacher
class Teacher(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


# This is an object for a course
# eache course has an year and each year has a curriculun
class Course(models.Model):
    name = models.CharField(max_length=150)
    code = models.IntegerField()
    year = models.CharField(max_length=10)
    # Podemos colocar catalogos
