from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, RedirectView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.http import is_safe_url
from django.conf import settings

import uuid
import os

from .forms import LoginForm, RegisterForm, UserInfoEditForm
from .models import BlogUser

# Create your views here.

class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

class MyLogoutView(LogoutView):
    pass

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        url = reverse('users:login')
        return HttpResponseRedirect(url)

class UserInfoEditView(UpdateView):
    form_class = UserInfoEditForm
    template_name = 'registration/edit.html'
    model = BlogUser
    pk_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        if self.request.user.pk != user_id:
            return HttpResponse(status=403) 
            
        user = get_object_or_404(BlogUser, pk=user_id)
        form = UserInfoEditForm(instance=user)
        return self.render_to_response({'user_id':user_id, 'form': form})

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        user_id = self.kwargs['user_id']
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        if self.request.user.pk != user_id:
            return HttpResponse(status=403) 

        self.object = form.save(commit=False)

        try:
            f = form.cleaned_data['upload_mugshot']
            imgextensions = ['.jpg', '.png', 'jpeg', '.gif']
            ext = None
            for e in imgextensions:
                if f.name.endswith(e):
                    ext = e
                    break
            if ext:
                imgfilename = str(uuid.uuid4().hex) + ext
                imgfilepath = os.path.join(
                    os.path.join(settings.MEDIA_ROOT, 'images'), 
                    imgfilename
                )
                fin = open(imgfilepath, 'wb+')
                for chunk in f.chunks():
                    fin.write(chunk)
                self.object.mugshot = os.path.join('images', imgfilename)
        except Exception as e:
            pass

        self.object.save()
            
        return redirect('/')

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        user_id = self.kwargs['user_id']
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        if self.request.user.pk != user_id:
            return HttpResponse(status=403)
        
        return self.render_to_response(self.get_context_data(form=form))