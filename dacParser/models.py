from django.db import models

# We should discuss all the models

# This object stores student
class Student(models.Model):
    name        = models.CharField(max_length=150)
    ra          = models.IntegerField()
    disciplines = models.ManyToManyField('Discipline')

    def __str__(self):
        return str(self.ra)+' - '+self.name

    # This method returns a string containing the path to the object
    def url(self):
        return '/s/'+str(self.ra)

    def AcademicEmail(self):
        firstLetter = self.name[0].lower()
        ra = str(self.ra)
        mail = '@dac.unicamp.br'
        return (firstLetter+ra+mail)

    # This is to avoid having two or more equal students, they are the same if
    # the name and RA are the same
    class Meta:
        unique_together = ["name", "ra"]

# This is the object thar stores subjects
class Discipline(models.Model):
    name        = models.CharField(max_length=150)
    code        = models.CharField(max_length=150)
    classes     = models.CharField(max_length=150)
    year        = models.CharField(max_length=5)
    semester    = models.CharField(max_length=2)
    teacher     = models.ForeignKey('Teacher',on_delete=models.CASCADE,)
    vacancies   = models.IntegerField()
    registered  = models.IntegerField()
    students    = models.ManyToManyField(Student)

    # To help on debug and kind of pretty
    def __str__(self):
        return self.code + ' '  + self.classes + ' - ' + self.name

    # This method returns a string containing the path to the object
    def url(self):
        return '/d/'+self.code+'/'+self.year+'/'+self.semester+'/'+self.classes

    # This is to avoid having two or more equal students, they are the same if
    # the name and RA are the same
    class Meta:
        unique_together = ["name", "code", "classes","year", "semester", "teacher"]

# This object stores the teacher
class Teacher(models.Model):
    name        = models.CharField(max_length=150)

    def __str__(self):
        return self.name
