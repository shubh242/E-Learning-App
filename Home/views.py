from django.shortcuts import render, reverse
from Client.models import Teacher
from Course.models import File, Attachment, Seminar, SeminarMessage, Course, Teacher , Event , Quiz, EventLink , EventImage, Upload, Message, SeminarMessage, Assignment, Submissions
import time
from django.utils import timezone
from datetime import datetime
import os
from django.conf import settings
import fnmatch
from Questions.models import Post
from Client.models import Subject, Student, Parent , Course
from django.http import HttpResponseRedirect
import os
import CodeEd.settings
from django.contrib.auth import login , logout , authenticate  
from django.contrib.auth.models import User
from django.contrib import messages
from .email import send_email
from Client.models import AdminStudent

# Create your views here.

def home(request):
    course = list(Course.objects.all())[::-1]
    subject = list(Subject.objects.all())[::-1]
    context = {}
    context['courses'] = course[:12]
    context['subjects'] = subject[:12]
    context['flag'] = False
    user = request.user
    if user.is_active:
        context['flag'] = True
    return render(request, 'home.html' , context)

def course_listed(request, pk):
    user = request.user
    subject = Subject.objects.get(id=pk)
    courses = subject.course_set.all()
    context = {}
    if request.method == "POST":
        term = request.POST['filter']
        subject = subject.filter(name__contains=term)
    context['courses'] = courses
    context['subject'] = subject
    return render(request, 'courses_listed.html', context)

def subjects_listed(request):
    context = {}
    subjects = Subject.objects.all()
    if request.method == "POST":
        term = request.POST['filter']
        subjects = subjects.filter(name__contains=term)
    context['subjects'] = subjects
    return render(request, 'subjects_listed.html', context)

def subjects_create(request):
    user = request.user
    context = {}
    context['valid'] = False
    if user.is_active:
        if len(list(Teacher.objects.all().filter(user=user))) > 0:
            teacher = Teacher.objects.all().filter(user=user)[0]
            context['valid'] = True
            if request.method == "POST":
                name = request.POST['name']
                description = request.POST['description']
                thumbnail = request.FILES['thumbnail']
                if thumbnail:
                    subject = Subject.objects.create(name=name, description=description, thumbnail=thumbnail)
                else:
                    subject = Subject.objects.create(name=name, description=description)
                return HttpResponseRedirect(reverse('subjects_listed'))
    return render(request, 'subject_create.html', context)

def user_login(request):
    context = {}
    context['log_try'] = False
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass1']
        print(username , password)
        user = authenticate(username= username , password = password)
        print(user)
        if user is not None:
            print('inside first if')
            if user.is_active:
                print('inside second if')
                login(request , user)
                context['log_try'] = True
                return HttpResponseRedirect(reverse('home'))
            else:
                print('nested Failed')
                return HttpResponseRedirect(reverse , 'login')
        else:
            messages.error(request , "Please enter the correct passowrd")
            return render(request , 'login.html')
    else:
        print('Post failed')
    return render(request , 'login.html')

def teacher_signup(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        email_id = request.POST['email']
        education = request.POST['education']
        branch = request.POST['branch']
        subject = request.POST['subject']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 == pass2:
            user = User.objects.create_user(username = username , email= email_id , password = pass1)
            teacher = Teacher.objects.create(user=user , name = user.username , branch=branch , education = education)
            subject = subject.split(',')
            for subjects in subject:
                sub , create = Subject.objects.get_or_create( name = subjects)
                teacher.subject.add(sub)
            print('Signup Success')
            return HttpResponseRedirect(reverse('login'))
        else:
            context['message'] = "Your passwords don't match"
    return render(request , 'teacher_signup.html' , context)

def check_otp(request, pk, otp):
    context = {}
    user = User.objects.get(id=pk)
    context['valid'] = False
    if request.method == 'POST':
        otp_re = int(request.POST['otp'])
        if otp == otp_re:
            context['valid'] = True
            student = Student.objects.all().filter(user=user)[0]
            adminstudent = AdminStudent.objects.all().filter(email=user.email)[0]
            for course in student.course.all():
                student.course.remove(course)
            for course in adminstudent.courses.all():
                student.course.add(course)
            return HttpResponseRedirect(reverse('login'))
    return HttpResponseRedirect(reverse('confirm_email', args=[user.id]))

import random
def confirm_email(request, pk):
    context = {}
    user = User.objects.get(id=pk)
    context['valid'] = False
    context['confirm'] = False
    context['user'] = user
    print(user.email)
    if len(list(AdminStudent.objects.filter(email=user.email))) > 0:
        context['valid'] = True
        print(user.email)
        otp = random.randint(1000,9999)
        send_email(user.email, otp)
        context['otp'] = otp
    return render(request, 'student_otp.html', context)


def student_signup(request):
    context = {}
    context['valid'] = True
    if request.method == "POST":
        print('inside post')
        username = request.POST['username']
        email_id = request.POST['email']
        if len(list(AdminStudent.objects.filter(email=email_id))) > 0:
            college = request.POST['college']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            if pass1 == pass2:
                print('nestedif')
                user = User.objects.create_user(username = username , email= email_id , password = pass1)
                print('nestedif2')
                student = Student.objects.create(user=user , name=user.username , college=college)
                print('Signup Success')
                return HttpResponseRedirect(reverse('login'))
            else:
                context['message'] = "Your passwords don't match"
        else:
            context['message'] = "You're not a registered student. Please contact Admin."
    print('post failed')
    return render(request , 'student_signup.html' , context)

def parent_signup(request):
    context = {}
    if request.method == "POST":
        print('outter if')
        username = request.POST['username']
        email_id = request.POST['email']
        child_name = request.POST['child_name']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context['flag'] = False
        if pass1 == pass2:
            print('nested if')
            user = User.objects.create_user(username = username , email= email_id , password = pass1)
            parent = Parent.objects.create(name=user.username , user=user)
            child_name = child_name.split(',')
            for students in child_name:
                print(type(students))
                try:
                    child , created = Student.objects.get_or_create(name=students)
                    parent.children.add(child)
                    print('Signup Success')
                    context['flag'] = True
                    return HttpResponseRedirect(reverse , 'home')
                except:
                    print('try Failed')
                    return render(request , 'parent_signup.html' , context)
        else:
            context['message'] = "Your passwords don't match"
    return render(request , 'parent_signup.html' , context)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('login'))

