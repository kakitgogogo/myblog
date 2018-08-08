from django.urls import path, include

from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery, name='index'), 
]