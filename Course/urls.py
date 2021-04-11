from django.urls import path
from .views import home,file_list
from .views import create_seminar, seminar, view_file,schedule,schedule_create, quiz_display, quiz_create, quiz_list, upload_list, seminar_detail, like_post_upload, create_course, user_course , Subject, show_read, create_assignment, assignment_list, submit_assignment
my_app = 'courses'

urlpatterns = [
    path('create/', create_course, name="create_course"),
    path('all/', user_course, name="user_course"),
    path('<int:pk>/seminar/create/', create_seminar, name="create_seminar"),
    path('<int:pk>/seminar/', seminar, name="seminar"),
    path('<int:cpk>/seminar/<int:spk>/', seminar_detail, name='seminar_detail'),
    path('<int:pk>/files/create/', file_list, name='file_list'),
    path('<int:pk>/files/', view_file, name='view_file'),
    path('<int:pk>/event/create/' ,schedule_create , name = 'event_create'),
    path('<int:pk>/events/',schedule , name = 'event_schedule'),
    path('<int:cpk>/quiz/<int:qpk>/detail/', quiz_display, name = 'quiz_display'),
    path('<int:pk>/quiz/create/', quiz_create, name = 'quiz_create'),
    path('<int:pk>/quiz/', quiz_list, name = 'quiz_list'),
    path('<int:pk>/uploads/', upload_list, name="upload_list"),
    path('<int:cpk>/<int:ppk>/uploads/', like_post_upload, name="upload_like"),
    path('attachment/<int:pk>/', show_read, name="show_read"),
    path('<int:pk>/assignment/create/', create_assignment, name="create_assignment"),
    path('<int:pk>/assignments/', assignment_list, name="assignment_list"),
    path('<int:pk>/submit_assignments/', submit_assignment, name="submit_assignment"),
]

