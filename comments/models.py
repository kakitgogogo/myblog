from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from blog.models import Post

# Create your models here.

class Comment(models.Model):
    body = models.TextField(_('body'))

    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    modified_time = models.DateTimeField(_('last modified time'), auto_now=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('commented post'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('author'), blank=True)
    superior = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_('superior comment'), blank=True, null=True)

    visiable = models.BooleanField('visiable', default=True)

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        get_latest_by = 'created_time'

    def __str__(self):
        return self.body[:20]