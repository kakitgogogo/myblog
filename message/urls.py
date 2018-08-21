from django.urls import path

from .import views

app_name = 'message'
urlpatterns = [
    path('<int:user_id>/', views.MessageView.as_view(), name='index')
]