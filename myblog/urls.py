"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve

import os

from blog.feeds import MyBlogFeed
from .admin import admin_site
from .settings import BASE_DIR
from blog.views import TechPostsView

urlpatterns = [
    path('', TechPostsView.as_view(), name='index'),
    path('', include('blog.urls')),
    path('comment/', include('comments.urls')),
    path('admin/', admin_site.urls),
    path('users/', include('users.urls')),
    path('oauth/', include('oauth.urls')),
    path('search/', include('haystack.urls')),
    path('all/rss/', MyBlogFeed(), name='rss'),
    path('gallery/', include('gallery.urls')),
    path('message/', include('message.urls')),
    url(r'^(?P<path>.*)$', serve, {'document_root': BASE_DIR}),
]
