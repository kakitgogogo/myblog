from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView
from django.utils.text import slugify
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import uuid
import os
import markdown
import json
from markdown.extensions.toc import TocExtension

from .models import Post, Category, Tag
from .forms import PostEditForm, UploadImageForm
from comments.forms import CommentForm

# Create your views here.
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    paginate_by = settings.PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.get_pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)

        return context

    def get_queryset(self):
        q = super(IndexView, self).get_queryset().all()
        if self.request.user.is_superuser:
            return q
        else:
            return q.filter(access_level='public')

    def get_pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []

        left_has_more = False
        right_has_more = False

        first = False
        last = False
        
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number : page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[((page_number - 3) if (page_number - 3) > 0 else 0) : page_number - 1]

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[((page_number - 3) if (page_number - 3) > 0 else 0) : page_number - 1]
            right = page_range[page_number : page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        return {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

class CategoryView(IndexView):
    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=category)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year, created_time__month=month)

class TechPostsView(IndexView):
    def get_queryset(self):
        return super(TechPostsView, self).get_queryset().exclude(category__name='game').exclude(category__name='daily')

class GamePostsView(IndexView):
    def get_queryset(self):
        return super(GamePostsView, self).get_queryset().filter(category__name='game')

class DailyPostsView(IndexView):
    def get_queryset(self):
        return super(DailyPostsView, self).get_queryset().filter(category__name='daily')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        # md = markdown.Markdown(extensions=[
        #     'markdown.extensions.extra',
        #     'markdown.extensions.codehilite',
        #     'markdown.extensions.fenced_code',
        #     # 'markdown.extensions.toc',
        #     TocExtension(slugify=slugify),
        # ])
        # post.body = md.convert(post.body)
        # post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.filter(visiable=True)
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context

class PostCreateView(CreateView):
    form_class = PostEditForm
    template_name = 'blog/create.html'
    model = Post

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        if not self.request.user.is_superuser:
            return redirect('users:login')

        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        tag_id_list = self.request.POST.getlist('tags')
        for tag_id in tag_id_list:
            self.object.tags.add(Tag.objects.get(pk=tag_id))
        self.object.save()
            
        return redirect(self.object)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        if not self.request.user.is_superuser:
            return redirect('users:login')
        
        return self.render_to_response(self.get_context_data(form=form))

class PostEditView(UpdateView):
    form_class = PostEditForm
    template_name = 'blog/edit.html'
    model = Post
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect('users:login')
            
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        form = PostEditForm(instance=post)
        return self.render_to_response({'post_id':post_id, 'form': form})

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        if not self.request.user.is_superuser:
            return redirect('users:login')

        self.object = form.save(commit=False)

        tag_id_list = self.request.POST.getlist('tags')
        self.object.tags.clear()
        for tag_id in tag_id_list:
            self.object.tags.add(Tag.objects.get(pk=tag_id))

        self.object.save()
            
        return redirect(self.object)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        if not self.request.user.is_superuser:
            return redirect('users:login')
        
        return self.render_to_response(self.get_context_data(form=form))

def json_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json") 

# editor.md： 上传图片
# 上传的后台只需要返回一个 JSON 数据，结构如下：
# {
# success : 0 | 1,           // 0 表示上传失败，1 表示上传成功
# message : "提示的信息，上传成功或上传失败及错误信息等。",
# url     : "图片地址"        // 上传成功时才返回
# }      
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        try:
            f = request.FILES['editormd-image-file']
            imgextensions = ['.jpg', '.png', 'jpeg', '.gif']
            ext = '.png'
            for e in imgextensions:
                if f.name.endswith(e):
                    ext = e
                    break
            imgfilename = str(uuid.uuid4().hex) + ext
            imgfilepath = os.path.join(
                os.path.join(settings.MEDIA_ROOT, 'images'), 
                imgfilename
            )
            fin = open(imgfilepath, 'wb+')
            for chunk in f.chunks():
                fin.write(chunk)
            return json_response({'success':1, 'message':'Successful upload', 'url':'/media/images/'+imgfilename})
        except Exception as e:
            pass
    return json_response({'success':0, 'message':'Failed upload'})

@csrf_exempt
def add_category(request):
    if request.method == 'POST' and request.user.is_superuser:
        try:
            new_category_name = request.POST.get('category')
            new_category = Category(name=new_category_name)
            new_category.save()    
            return json_response({'success':1, 'id':new_category.pk, 'name':new_category.name})
        except:
            pass
    return json_response({'success':0})
    
@csrf_exempt
def add_tag(request):
    if request.method == 'POST' and request.user.is_superuser:
        try:
            new_tag_name = request.POST.get('tag')
            new_tag = Tag(name=new_tag_name)
            new_tag.save()    
            return json_response({'success':1, 'id':new_tag.pk, 'name':new_tag.name})
        except:
            pass
    return json_response({'success':0})
    