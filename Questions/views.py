from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Post, Comment, Subject, PostImage, Course, Notification, Student
from Client.models import Teacher
from Course.models import Upload
from django.urls import reverse

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

# Post List:
def posts(request):
    context = {}
    post_list = []
    for post in Post.objects.all():
        if list(post.postimage_set.all()) != []:
            post_list.append((post, list(post.postimage_set.all())[0]))
        else:
            post_list.append((post, None))
    context['questions'] = post_list
    return render(request, 'posts.html', context)

# Post Detail:
def post_detail(request, pk):
    context = {}
    user = request.user
    post = Post.objects.get(id=pk)
    if user.is_active:
        if request.method == 'POST':
            content = request.POST['comment']
            print(content)
            comment = Comment.objects.create(content=content, user=user, post=post)
    comments = post.comment_set.all().order_by('-timestamp')
    context['post'] = post
    context['comments'] = comments
    context['post_images'] = post.postimage_set.all()
    return render(request, 'post_detail.html', context)

# Post Create:
def post_create(request):
    context = {}
    subjects = Subject.objects.all()
    context['subjects'] = subjects
    course = Course.objects.all()
    context['courses'] = course
    user = request.user
    if user.is_active:
        if request.method == 'POST':
            content = request.POST['question']
            subject_name = request.POST['subject']
            subject = Subject.objects.all().get(id=subject_name)
            post = Post.objects.create(question=content, user=user)
            post.subject.add(subject)
            course_name = request.POST['subject']
            course = Course.objects.all().get(id=course_name)
            post.course.add(course)
            Upload.objects.create(post_upload=post, course=course)
            notif = Notification.objects.create(post=post)
            for teach in course.teacher.all():
                notif.teacher.add(teach)
            for teach in subject.teacher_set.all():
                notif.teacher.add(teach)
            for i in range(1, 7):
                try:
                    name = 'image-' + str(i)
                    image = request.FILES[name]
                    PostImage.objects.create(post=post, image=image)
                except:
                    break
    return render(request, 'post_create.html', context)

#Like Comment:
def like_post(request, pk):
    user = request.user
    if user.is_active:
        post = Post.objects.get(id=pk)
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
    return HttpResponseRedirect(reverse('posts'))

#Like Comment:
def like_comment(request, ppk, cpk):
    user = request.user
    if user.is_active:
        comment = Comment.objects.get(id=cpk)
        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(ppk)]))

# Notifications List View:
def view_notifications(request):
    user = request.user
    context = {}
    context['valid'] = False
    context['valid_student'] = False
    context['valid_teacher'] = False
    try:
        if len(list(Teacher.objects.filter(user=user))) > 0:
            teacher = Teacher.objects.filter(user=user)[0]
            notifs = Notification.objects.all().filter(teacher=teacher)
            context['notifications'] = notifs
            context['valid_teacher'] = True
            context['valid'] = True
        else:
            notifs = []
            if len(list(Student.objects.all().filter(user=user))) > 0:
                student = Student.objects.all().filter(user=user)[0]
                for course in Course.objects.all().filter(student = student):
                    uploads = Upload.objects.all().filter(course=course)
                    context['uploads'] = uploads
                    context['valid_student'] = True
                    context['valid'] = True
    except:
        pass
    return render(request, 'notifications.html', context)

        


