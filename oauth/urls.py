from django.urls import path, include

from . import views

app_name = 'oauth'

urlpatterns = [
    path('authorize', views.authorize, name='authorize'),
]