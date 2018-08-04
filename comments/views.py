from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.http import Http404

from blog.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {
                'post': post, 
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)
    
    return redirect(post)

class CommentView(FormView):
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        return redirect(post.get_absolute_url() + "#comment-area")

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        if not self.request.user.is_authenticated:
            return redirect('users:login')

        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)

        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user

        if form.cleaned_data['superior_id']:
            comment.superior = Comment.objects.get(pk=form.cleaned_data['superior_id'])

        comment.save()
            
        return redirect(post)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        if not self.request.user.is_authenticated:
            return redirect('users:login')

        user = self.request.user
        post_id = self.kwargs['post_id']
        
        return self.render_to_response(self.get_context_data(form=form))
        

