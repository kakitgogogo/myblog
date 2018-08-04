from django.contrib import admin
from .models import Post, Category, Tag
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'created_time', 'modified_time']
    list_display_links = ('id', 'title')
    exclude = ['created_time', 'modified_time', 'views']

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')    

