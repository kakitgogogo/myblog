from django.contrib.admin import AdminSite
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin 
from django.contrib.admin.models import LogEntry

from users.admin import *
from oauth.admin import *
from blog.admin import *
from comments.admin import *

class BlogAdminSite(AdminSite):
    site_header = 'Blog administration'
    site_title = 'Blog site admin'

    def __init__(self, name='admin'):
        super().__init__(name)

    def has_permission(self, request):
        return request.user.is_superuser

admin_site = BlogAdminSite(name='admin')

admin_site.register(BlogUser, UserAdmin)
admin_site.register(OAuthUser, OAuthUserAdmin)
admin_site.register(Post, PostAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(Comment, CommentAdmin)

admin_site.register(Site, SiteAdmin)
