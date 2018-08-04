from django.contrib import admin

# Register your models here.
from .models import BlogUser

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'username', 'email', 'last_login', 'date_joined')
    list_display_links = ('id', 'username') 
    exclude = ['password']