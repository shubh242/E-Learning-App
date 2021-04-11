from django.contrib import admin
from .models import Post, PostImage, Comment, Notification

# Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Comment)
admin.site.register(Notification)
