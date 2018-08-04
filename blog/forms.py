from django import forms
from django.forms import widgets

from .models import Post, Category, Tag

class PostEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget = widgets.TextInput(
            attrs={'class': 'form-control','style': 'width:50%;'})
        self.fields['body'].widget = widgets.Textarea(
            attrs={'style': 'display:none;'})
        self.fields['category'].widget.attrs={'class': 'form-control','style': 'width:50%;'}
        self.fields['tags'].widget.attrs={'class': 'form-control','style': 'width:50%;'}
        self.fields['access_level'].widget.attrs={'class': 'form-control','style': 'width:50%;'}  

    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'tags', 'access_level', 'sticky']

class UploadImageForm(forms.Form):
    image = forms.ImageField()
