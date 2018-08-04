from django.urls import path, include

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.TechPostsView.as_view(), name='index'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archive/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'), 
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('category/add/', views.add_category, name='add_category'),
    path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('tag/add/', views.add_tag, name='add_tag'),    
    path('game/', views.GamePostsView.as_view(), name='game'), 
    path('daily/', views.DailyPostsView.as_view(), name='daily'),    
    path('create/post', views.PostCreateView.as_view(), name='create'),
    path('edit/post/<int:post_id>/', views.PostEditView.as_view(), name='edit'),
    path('upload/image', views.upload_image, name='upload_image')
]