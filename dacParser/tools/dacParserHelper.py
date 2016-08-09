# This is the object thar stores subjects
class Discipline(object):
    name = ""
    code = ""
    year = ""
    semester = ""
    classes = ""
    teacher = ""
    vacancies = 0
    registered = 0
    students = object

    def __init__(self, name, code, classes, year, semester, teacher, vacancies,
                 registered, students):
        self.name = name
        self.code = code
        self.classes = classes
        self.year = year
        self.semester = semester
        self.teacher = teacher
        self.vacancies = vacancies
        self.registered = registered
        self.students = students

    # TO help on debug and kind of pretty
    def __str__(self):
        beautiprint = '''
        Name        : %s
        Code        : %s
        Classes     : %s
        Year        : %s
        Semester    : %s
        Teacher     : %s
        Regis/Vacan : %s/%s
        Students    : %s
        '''
        return (beautiprint %
                (self.name, self.code, self.classes, self.year, self.semester,
                 self.teacher, self.registered, self.vacancies,
                 self.students))

    # Return True if the student is in this discipline
    def searchStudentName(self, studentName):
        for student in self.students:
            if(studentName == student[1]):
                return True
        return False

    # Return True if the student is in this discipline
    def searchStudentRA(self, studentRA):
        for student in self.students:
            if(studentName == student[0]):
                return True
        return False

    # Generate a list tha contains all the dac mail from the students
    def generateAcademicEmail(self):
        mailList = []
        for student in self.students:
            firstLetter = student[1][0].lower()
            ra = str(student[0])
            mail = '@dac.unicamp.br'
            mailList.append(firstLetter+ra+mail)
        return mailList
