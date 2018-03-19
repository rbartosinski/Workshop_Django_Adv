from django.db import models

SCHOOL_CLASS = (
    (1, "1a"),
    (2, "1b"),
    (3, "2a"),
    (4, "2b"),
)

GRADES = (
    (1, "1"),
    (1.5, "1+"),
    (1.75, "2-"),
    (2, "2"),
    (2.5, "2+"),
    (2.75, "3-"),
    (3, "3"),
    (3.5, "3+"),
    (3.75, "4-"),
    (4, "4"),
    (4.5, "4+"),
    (4.75, "5-"),
    (5, "5"),
    (5.5, "5+"),
    (5.75, "6-"),
    (6, "6")
)


class SchoolSubject(models.Model):
    name = models.CharField(max_length=64)
    teacher_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name + ' ' + self.teacher_name


class Student(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    school_class = models.IntegerField(choices=SCHOOL_CLASS)
    grades = models.ManyToManyField(SchoolSubject, through="StudentGrades")  # subjects
    year_of_birth = models.IntegerField(null=True)

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.name


class StudentGrades(models.Model):
    student = models.ForeignKey(Student)
    school_subject = models.ForeignKey(SchoolSubject)
    grade = models.FloatField(choices=GRADES)


class PresenceList(models.Model):
    student = models.ForeignKey(Student)
    day = models.DateField()
    present = models.NullBooleanField()


class Message(models.Model):
    subject = models.CharField(max_length=256)
    content = models.TextField()
    to = models.ForeignKey(SchoolSubject)
    from_fk = models.ForeignKey(Student)
    date_sent = models.DateTimeField(auto_now_add=True)


class StudentNotice(models.Model):
    from_fk = models.ForeignKey(SchoolSubject)
    to = models.ForeignKey(Student)
    content = models.TextField()