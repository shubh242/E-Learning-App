from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
    name = models.TextField(max_length=30)
    description = models.TextField(max_length=300, blank=True)
    thumbnail = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.TextField(max_length=100)
    subject = models.ManyToManyField(Subject, blank=True)
    branch = models.TextField(max_length=100, blank=True)
    education = models.TextField(max_length=300, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.TextField(max_length=100)
    subject = models.ManyToManyField(Subject, blank=True)
    teacher = models.ManyToManyField(Teacher, blank=True)
    thumbnail = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.FloatField(blank=True)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.course.name

class Student(models.Model):
    name = models.TextField(max_length=100)
    college = models.TextField(max_length=100)
    course = models.ManyToManyField(Course, blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(blank=True)
    maximum = models.IntegerField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.name

class Parent(models.Model):
    name = models.TextField(max_length=100)
    children = models.ManyToManyField(Student, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Administrator(models.Model):
    name = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AdminStudent(models.Model):
    email = models.TextField(max_length=100)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.email

class AdminTeacher(models.Model):
    email = models.TextField(max_length=100)

    def __str__(self):
        return self.email

class AdminParent(models.Model):
    email = models.TextField(max_length=100)

    def __str__(self):
        return self.email