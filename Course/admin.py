from django.contrib import admin
from .models import File, Attachment, Seminar, Event, EventImage, EventLink, Quiz, Upload, Message, SeminarMessage, Assignment, Submissions


# Register your models here.
admin.site.register(File)
admin.site.register(Attachment)
admin.site.register(Seminar)
admin.site.register(Event)
admin.site.register(EventImage)
admin.site.register(EventLink)
admin.site.register(Quiz)
admin.site.register(Upload)
admin.site.register(Message)
admin.site.register(SeminarMessage)
admin.site.register(Assignment)
admin.site.register(Submissions)