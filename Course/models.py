from django.db import models
from Client.models import Course, Teacher, Student
from django.contrib.auth.models import User
from Questions.models import Post

# Create your models here.

# Files:
class File(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    
class Attachment(models.Model):
    files = models.ForeignKey(File, on_delete=models.CASCADE)
    attach = models.FileField(upload_to='files', blank=True)
    context = models.TextField(blank=True)
    name = models.TextField(max_length=100, blank=True, null=True)
    converted = models.BooleanField(default=False)

# Seminars:
class Seminar(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos')
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to="thumbnail",blank=True,null=True)

class SeminarMessage(models.Model):
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)

# Schedules:
class Event(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.TextField(max_length=100)
    description = models.TextField()
    event_timestamp = models.DateTimeField(blank=True, null=True)
    event_timestamp_end = models.TimeField(blank=None , null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    link = models.TextField(max_length=100)

class EventImage(models.Model):
    image = models.ImageField(upload_to='event_images')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class EventLink(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    link = models.TextField(max_length=300)

#Quizes:
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    embed_link = models.TextField(max_length=300)
    title = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    enable = models.DateTimeField()

class Message(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Assignment(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=300)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    files = models.FileField(upload_to='assignments', blank=True, null=True)
    deadline = models.DateTimeField()

class Submissions(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    files = models.FileField(upload_to='submissions', blank=True, null=True)
    after_deadline = models.BooleanField()

class Upload(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file_upload = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    event_upload = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    seminar_upload = models.ForeignKey(Seminar, on_delete=models.CASCADE, null=True, blank=True)
    quiz_upload = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    message_upload = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    post_upload = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    assignment_upload = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
