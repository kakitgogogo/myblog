from django.contrib import admin

from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'has_read', 'created_time')
    list_display_links = ('id',)
