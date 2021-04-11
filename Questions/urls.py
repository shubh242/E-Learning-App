from django.urls import path
from .views import home, posts, post_detail,post_create, like_comment, like_post, view_notifications

urlpatterns = [
    path('', home, name="home"),
    path('posts', posts, name='posts'),
    path('posts/<int:pk>', post_detail, name='post_detail'),
    path('posts/create', post_create, name='post_create'),
    path('posts/comment/like/<int:ppk>/<int:cpk>', like_comment, name="comment_like"),
    path('posts/like/<int:pk>', like_post, name="post_like"),
    path('notifications', view_notifications, name="view_notifications"),
]
