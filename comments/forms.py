from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    superior_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['body']