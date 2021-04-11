from django.urls import path
from .views import course_listed, subjects_listed, subjects_create, user_login, user_logout, teacher_signup, student_signup, parent_signup, confirm_email, check_otp , home

urlpatterns = [
    path('',home,name="home"),
    path('subjects', subjects_listed, name="subjects_listed"),
    path('subjects/create', subjects_create, name="subjects_create"),
    path('<int:pk>/courses', course_listed, name="course_listed"),
    path('login/', user_login, name="login"),
    path('logout/' , user_logout , name = "logout"),
    path('teacher_signup/', teacher_signup, name="teacher_signup"),
    path('student_signup/', student_signup, name="student_signup"),
    path('parent_signup/', parent_signup, name="parent_signup"),
    path('<int:pk>/confirm_email/', confirm_email, name="confirm_email"),
    path('<int:pk>/<int:otp>/confirm_email/', check_otp, name="check_otp"),
]