from django.db import models
from Client.models import Student, Parent, Teacher, Subject, Course
from django.contrib.auth.models import User

class Post(models.Model):
    question = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject, blank=True)
    course = models.ManyToManyField(Course, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='postlike')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.question

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='PostImages')

class Comment(models.Model):
    content = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='commentlike')
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    teacher = models.ManyToManyField(Teacher, blank=True)


