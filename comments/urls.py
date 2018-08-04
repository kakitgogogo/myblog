from django.urls import path

from .import views

app_name = 'comments'
urlpatterns = [
    path('post/<int:post_id>/', views.CommentView.as_view(), name='post_comment')
]