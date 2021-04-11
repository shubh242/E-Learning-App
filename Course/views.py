from django.shortcuts import render, reverse
from Client.models import Teacher
from .models import File, Attachment, Seminar, SeminarMessage, Course, Teacher , Event , Quiz, EventLink , EventImage, Upload, Message, SeminarMessage, Assignment, Submissions
import time
from django.utils import timezone
from datetime import datetime
import os
from django.conf import settings
import fnmatch
from Questions.models import Post
from Client.models import Subject, Student, Parent
from django.http import HttpResponseRedirect
from .operations import read_image
import os
import CodeEd.settings
from django.contrib.auth import login , logout , authenticate  
from django.contrib.auth.models import User
from django.contrib import messages
from Client.models import AdminStudent
# Create your views here. 

def home(request):
    course = Course.objects.all()
    context = {}
    context['courses'] = course
    return render(request, 'home.html',context)

def file_list(request, pk):
    user = request.user
    print('hi')
    context = {}
    context['valid'] = False
    print(len(list(Teacher.objects.all().filter(user=user))))
    if len(list(Teacher.objects.all().filter(user=user))) > 0:
        context['valid'] = True
    user = request.user
    if request.method == "POST":
        if user.is_active:
            file_description = request.POST["file_description"]
            file_name = request.POST["name"]
            course = Course.objects.get(id=pk)
            context['course'] = course
            if len(list(Teacher.objects.all().filter(user=user))) > 0:
                context['valid'] = True
                teacher = Teacher.objects.filter(user=user)[0]
                file_instance = File.objects.create(course=course, teacher=teacher, name=file_name, description=file_description)
                upload = Upload.objects.create(course=course, file_upload=file_instance)
                convert = request.POST['convert']
                for i in range(1, 5):
                    try:
                        name = 'file-' + str(i)
                        attached_file = request.FILES[name]
                        name2 = 'file-text-' + str(i)
                        attached_file_text = request.POST[name2]
                        Attachment.objects.create(files=file_instance, attach=attached_file, name=attached_file_text)
                    except:
                        pass
                if convert == "True":
                    for attach in file_instance.attachment_set.all():
                        text = read_image(attach.attach)
                        Attachment.objects.create(files=file_instance, name=attach.name + ' - Converted', context=text, converted=True)
        return render(request, 'files_create.html', context)
    return render(request, 'files_create.html', context)

def create_seminar(request, pk):
    user = request.user
    context = {}
    context['success'] = False 
    context['valid'] = False
    if request.method == 'POST':
        if user.is_active:
            if len(list(Teacher.objects.filter(user=user))) > 0:
                context['valid'] = True
                teacher = Teacher.objects.filter(user=user)[0]
                course = Course.objects.get(id=pk)
                context['course'] = course
                name = request.POST['name']
                description = request.POST['description']
                video = request.FILES['video']
                seminar = Seminar.objects.create(course=course, teacher=teacher, name=name, description=description, video=video)
                upload = Upload.objects.create(course=course, seminar_upload=seminar)
                context['success'] = True
    return render(request, 'seminar_create.html', context)
        
def seminar(request,pk):
    context = {}
    course= Course.objects.get(id=pk)
    seminar_set = Seminar.objects.all().filter(course=course)
    context['course'] = course
    user = request.user
    context['valid'] = False
    context['valid_user'] = False
    if user.is_active:
        if len(list(Teacher.objects.all().filter(user=user))) > 0:
            context['valid'] = True
            context['valid_user'] = True
        student = None
        try:
            student = Student.objects.get(user=user)
        except:
            pass
        if student: 
            if course in Student.objects.get(user=user).course.all():
                context['valid_user'] = True
    if request.method == "POST":
        term = request.POST['filter']
        seminar_set = seminar_set.filter(name__contains=term)
    context['Seminars'] = seminar_set
    return render(request, 'seminar.html', context)

def view_file(request,pk):
    context = {}
    course= Course.objects.get(id=pk)
    context['course'] = course
    files_list = []
    files_set = File.objects.all().filter(course=course)
    user = request.user
    context['valid'] = False
    context['valid_user'] = False
    if user.is_active:
        if len(list(Teacher.objects.all().filter(user=user))) > 0:
            context['valid'] = True
            context['valid_user'] = True
        student = None
        try:
            student = Student.objects.get(user=user)
        except:
            pass
        if student: 
            if course in Student.objects.get(user=user).course.all():
                context['valid_user'] = True
    if request.method == "POST":
        term = request.POST['filter']
        files_set = files_set.filter(name__contains=term)
    for item in files_set:
        files_list.append((item, item.attachment_set.all()))
    context['files'] = files_list
    return render(request, 'view_file.html', context)

def schedule(request,pk):
    context = {}
    course = Course.objects.get(id = pk)
    context['course'] = course
    event_list = []
    user = request.user
    context['valid'] = False
    context['valid'] = False
    context['valid_user'] = False
    if user.is_active:
        if len(list(Teacher.objects.all().filter(user=user))) > 0:
            context['valid'] = True
            context['valid_user'] = True
        student = None
        try:
            student = Student.objects.get(user=user)
        except:
            pass
        if student: 
            if course in Student.objects.get(user=user).course.all():
                context['valid_user'] = True
    for items in Event.objects.all().filter(course = course):
        event_list.append((items , items.eventimage_set.all()))
    context["events"] = event_list
    return render(request , 'event_schedule.html' , context)

def schedule_create(request,pk):
    user = request.user
    context = {}
    context["success"] = False
    context['valid'] = False
    if request.method == "POST":
        if user.is_active:
            if len(list(Teacher.objects.filter(user = user))) > 0:
                context['valid'] = True
                teacher = Teacher.objects.filter(user = user)[0]
                course = Course.objects.get(id = pk)
                context['course'] = course
                name = request.POST["event_name"]
                description = request.POST["event_description"]
                time = request.POST["event_start"]
                event_link = request.POST["event_link"]
                event_instance = Event.objects.create(course=course , teacher=teacher , name = name , description=description , event_timestamp=datetime.strptime(time , '%Y-%m-%dT%H:%M'))
                upload = Upload.objects.create(course=course, event_upload=event_instance)
                EventLink.objects.create(event=event_instance , link=event_link)
                name = 'event_image-1'
                image = request.FILES[name]
                EventImage.objects.create(image = image , event = event_instance)
                context["success"] = True
    return render(request , "event_create.html")

def quiz_display(request, cpk, qpk):
    context = {}
    course = Course.objects.get(id=cpk)
    context['course'] = course
    quiz = course.quiz_set.all().get(id=qpk)
    context['quiz'] = quiz
    context['valid'] = False
    user = request.user
    context['valid_user'] = False
    if user.is_active:
        if len(list(Teacher.objects.all().filter(user=user))) > 0:
            context['valid'] = True
            context['valid_user'] = True
        student = None
        try:
            student = Student.objects.get(user=user)
        except:
            pass
        if student: 
            if Student.objects.get(user=user) in course.student_set.all():
                context['valid_user'] = True
    return render(request, 'quiz.html', context)

def quiz_create(request, pk):
    context = {}
    user = request.user
    course = Course.objects.get(id=pk)
    context['course'] = course
    context['valid'] = False
    if len(list(Teacher.objects.all().filter(user=user))) > 0:
        teacher = Teacher.objects.all().filter(user=user)[0]
        context['valid'] = True
        if request.method == 'POST':
            name = request.POST['name']
            url = request.POST['url'] + 'viewform?embedded=true'
            time = request.POST['quiz_start']
            embed = Quiz.objects.create(course=course, teacher=teacher, title=name, embed_link=url, enable=datetime.strptime(time, '%Y-%m-%dT%H:%M'))
            upload = Upload.objects.create(course=course, quiz_upload=embed)
    return render(request, 'quiz_create.html', context)

def quiz_list(request, pk):
    context = {}
    course = Course.objects.get(id=pk)
    context['course'] = course
    quizes = course.quiz_set.all().order_by('enable')
    quiz_list = []
    user = request.user
    context['valid_user'] = False
    if user.is_active:
        if len(list(Teacher.objects.all().filter(user=user))) > 0:
            context['valid'] = True
            context['valid_user'] = True
        student = None
        try:
            student = Student.objects.get(user=user)
        except:
            pass
        if student: 
            if course in Student.objects.get(user=user).course.all():
                context['valid_user'] = True
    if request.method == "POST":
        term = request.POST['filter']
        quizes = quizes.filter(title__contains=term)
    for quiz in quizes:
        if quiz.enable >= timezone.now():
            quiz_list.append((quiz, True))
    for quiz in quizes.reverse():
        if quiz.enable < timezone.now():
            quiz_list.append((quiz, False))
    context['course_id'] = course.id
    context['quizes'] = quiz_list
    return render(request, 'quiz_list.html', context)

def upload_list(request, pk):
    context = {}
    context['course_id'] = pk
    course = Course.objects.get(id=pk)
    uploads = Upload.objects.all().filter(course=course).order_by('-timestamp')
    context['course'] = course
    context['uploads'] = uploads
    user = request.user
    context['valid'] = False
    context['valid_user'] = False
    if user.is_active:
        if len(list(Teacher.objects.all().filter(user=user))) > 0:
            context['valid'] = True
            context['valid_user'] = True
        student = None
        try:
            student = Student.objects.get(user=user)
        except:
            pass
        if student: 
            if course in Student.objects.get(user=user).course.all():
                context['valid_user'] = True
        if request.method == "POST":
            message = request.POST['message']
            message_instance = Message.objects.create(user=user, course=course, content=message)
            Upload.objects.create(message_upload = message_instance, course=course)
    return render(request, 'uploads.html', context)

def seminar_detail(request, cpk, spk):
    user = request.user
    context = {}
    if user.is_active:
        course = Course.objects.get(id=cpk)
        seminar = Seminar.objects.get(id=spk)
        context['course'] = course
        context['seminar'] = seminar
        context['valid'] = False
        context['valid_user'] = False
        if user.is_active:
            if len(list(Teacher.objects.all().filter(user=user))) > 0:
                context['valid'] = True
                context['valid_user'] = True
            student = None
            try:
                student = Student.objects.get(user=user)
            except:
                pass
            if student: 
                if course in Student.objects.get(user=user).course.all():
                    context['valid_user'] = True
        if request.method == "POST":
            comment = request.POST['comment']
            SeminarMessage.objects.create(user=user, content=comment, seminar=seminar)
        comm = list(SeminarMessage.objects.all().filter(seminar=seminar))
        comm.reverse()
        context['comments'] = comm
        url = 'http://127.0.0.1:8000' + seminar.video.url
        print(url)
        context['url'] = url
    return render(request, 'seminar_detail.html', context)

def like_post_upload(request, cpk, ppk):
    user = request.user
    context = {}
    if user.is_active:
        post = Post.objects.get(id=ppk)
        course = Course.objects.get(id=cpk)
        upload = Upload.objects.all().filter(course=course).order_by('-timestamp')
        context['uploads'] = upload
        context['course'] = course
        context['valid'] = False
        context['valid_user'] = False
        if user.is_active:
            if len(list(Teacher.objects.all().filter(user=user))) > 0:
                context['valid'] = True
                context['valid_user'] = True
            student = None
            try:
                student = Student.objects.get(user=user)
            except:
                pass
            if student: 
                if course in Student.objects.get(user=user).course.all():
                    context['valid_user'] = True
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
    return render(request, 'uploads.html', context)

def create_course(request):
    user = request.user
    context = {}
    context['valid'] = False
    if user.is_active:
        if len(list(Teacher.objects.filter(user=user))) > 0:
            teacher = Teacher.objects.filter(user=user)[0]
            context['valid'] = True
            subjects = Subject.objects.all()
            context['subjects'] = subjects
            if request.method == "POST":
                name = request.POST['name']
                subject = request.POST['subject']
                thumbnail = request.POST['thumbnail']
                if thumbnail:
                    course = Course.objects.create(name=name, thumbnail=thumbnail)
                else:
                    course = Course.objects.create(name=name)
                course.teacher.add(teacher)
                course.subject.add(subject)
                return HttpResponseRedirect(reverse('upload_list', args=[int(course.id)]))
    return render(request, 'course_form.html', context)

def user_course(request):
    user = request.user
    context = {}
    context['valid'] = False
    if len(list(Teacher.objects.all().filter(user=user))) > 0:
        context['valid'] = True
    if user.is_active:
        courses = []
        try:
            if len(list(Teacher.objects.filter(user=user))) > 0:
                teacher = Teacher.objects.filter(user=user)[0]
                courses = teacher.course_set.all()
            elif len(list(Student.objects.filter(user=user))) > 0:
                student = Student.objects.filter(user=user)[0]
                courses = student.course.all()
            elif len(list(Parent.objects.filter(user=user))) > 0:
                parent = Parent.objects.filter(user=user)[0]
                students = parent.children.all()
                course_set = []
                for student in students:
                    courses_i = student.course.all() 
                    course_set.extend(list(courses_i))
                courses = course_set
            else:
                context['valid'] = False
        except:
            pass
        context['courses'] = courses 
    return render(request, 'course_list.html', context)

def show_read(request, pk):
    attachment = Attachment.objects.get(id=pk)
    context = {}
    context['attachment'] = attachment
    context['content'] = attachment.context
    return render(request, 'attachment_display.html', context)

def create_assignment(request, pk):
    user = request.user
    context = {}
    context['valid'] = False
    if len(list(Teacher.objects.all().filter(user=user))) > 0 :
        context['valid'] = True
        teacher = Teacher.objects.all().filter(user=user)[0]
        if request.method == "POST":
            course = Course.objects.get(id=pk)
            name = request.POST['name']
            description = request.POST['description']
            file_istance = request.FILES['file']
            deadline = request.POST['time']
            if file_istance:
                assignment = Assignment.objects.create(course=course, name=name, description=description, files=file_istance, teacher=teacher, deadline=datetime.strptime(deadline , '%Y-%m-%dT%H:%M'))
            else:
                assignment = Assignment.objects.create(course=course, name=name, description=description, teacher=teacher)
            Upload.objects.create(course=course, assignment_upload=assignment)
        return render(request, 'create_assignment.html', context)

def assignment_list(request, pk):
    user = request.user
    context = {}
    context['valid'] = False
    context['valid_teacher'] = False
    flag = False
    course = Course.objects.all().get(id=pk)
    context['course'] = course
    if user in list(User.objects.all()):
        if len(list(Student.objects.all().filter(user=user))) > 0:
            student = Student.objects.all().filter(user=user)[0]
            if student in course.student_set.all():
                context['valid'] = True
                context['assignments'] = course.assignment_set.all()
                if request.method == 'POST':
                    assignment_id = request.POST['assignment']
                    file_instance = request.FILES['submission']
                    assignment = Assignment.objects.get(id=assignment_id)
                    if timezone.now() > assignment.deadline:
                        Submissions.objects.create(assignment=assignment, student=student, files=file_instance, after_deadline = True)
                    else:
                        Submissions.objects.create(assignment=assignment, student=student, files=file_instance, after_deadline = False)
        elif len(list(Teacher.objects.all().filter(user=user))) > 0:
            teacher = Teacher.objects.all().filter(user=user)[0]
            context['valid'] = True
            context['valid_teacher'] = True
            context['assignments'] = course.assignment_set.all()
            if request.method == 'POST':
                assignment_id = request.POST['assignment']
                file_instance = request.FILES['submission']
                assignment = Assignment.objects.get(id=assignment_id)
                if timezone.now() > assignment.deadline:
                    Submissions.objects.create(assignment=assignment, student=student, files=file_instance, after_deadline = True)
                else:
                    Submissions.objects.create(assignment=assignment, student=student, files=file_instance, after_deadline = False)
    return render(request, 'assignment_list.html', context)

def submit_assignment(request, pk):
    if request.method == 'POST':
        assignment = Assignment.objects.get(id=pk)
        name = str(pk) + 'files'
        file_instance = request.FILES.get(name)
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        user = request.user
        student = Student.objects.all().filter(user=user)[0]
        if timezone.now() > assignment.deadline:
            Submissions.objects.create(assignment=assignment, student=student, files=file_instance, after_deadline = True)
        else:
            Submissions.objects.create(assignment=assignment, student=student, files=file_instance, after_deadline = False)
        if course_id == None:
            course_id = 1
        return HttpResponseRedirect(reverse('assignment_list', args=[int(course_id)]))