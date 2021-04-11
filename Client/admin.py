from django.contrib import admin
from .models import Score, Student, Subject, Rating, Teacher, Course, Parent, AdminParent, AdminStudent, AdminTeacher, Administrator

# Register your models here.
admin.site.register(Score)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Rating)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Parent)
admin.site.register(AdminParent)
admin.site.register(AdminStudent)
admin.site.register(AdminTeacher)