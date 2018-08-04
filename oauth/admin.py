from django.contrib import admin
from .models import OAuthUser

# Register your models here.

class OAuthUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid', 'platform')
    list_display_links = ('id', 'userid')
