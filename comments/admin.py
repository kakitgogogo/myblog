from django.contrib import admin

from .models import Comment
# Register your models here.

def disable_comments(modeladmin, request, queryset):
    queryset.update(visiable=False)

def enable_comments(modeladmin, request, queryset):
    queryset.update(visiable=True)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'body', 'author', 'visiable', 'post', 'modified_time')
    list_display_links = ('id', 'body')
    actions = [disable_comments, enable_comments]