from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from django.forms import widgets

from .models import BlogUser

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': 'username', 'class': 'text'})       
        self.fields['email'].widget = widgets.EmailInput(
            attrs={'placeholder': "email", "class": "text"})
        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "text"})
        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={'placeholder': "repeat password", "class": "text"})

    class Meta:
        model = BlogUser
        fields = ('username', 'email', 'nickname', 'mugshot')

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': 'username or email', 'class': 'text'})
        self.fields['password'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "text"})

    error_messages = {
        'invalid_login': 
            "Please enter a correct username and password. Note that both "
            "fields may be case-sensitive."
        ,
        'inactive': "This account is inactive.",
    }

class UserInfoEditForm(forms.ModelForm):
    upload_mugshot = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserInfoEditForm, self).__init__(*args, **kwargs)

        self.fields['nickname'].widget = widgets.TextInput(
            attrs={'placeholder': '昵称', 'class': 'form-control'})       
        self.fields['email'].widget = widgets.EmailInput(
            attrs={'placeholder': "电子邮箱", "class": "form-control"})
        self.fields['upload_mugshot'].widget = widgets.FileInput(
            attrs={"id": "mugshot"})

    class Meta:
        model = BlogUser
        fields = ('email', 'nickname')