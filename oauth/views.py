from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login

from .backend import get_oauth_backend

# Create your views here.

def authorize(request):
    platform = request.GET.get('platform', None)
    login_url = reverse('users:login')
    if not platform:
        return redirect(login_url)
    backend = get_oauth_backend(platform)
    if not backend:
        return redirect(login_url)
    code = request.GET.get('code', None)
    if not code:
        return redirect(login_url)
    next_url = request.GET.get('next', None)
    if not next_url:
        next_url = '/'
    access_token = backend.get_access_token(code)
    if not access_token:
        return redirect(login_url)
    user = backend.get_user_info()
    if not user:
        return redirect(login_url)
    login(request, user)
    return redirect(next_url)


    
    