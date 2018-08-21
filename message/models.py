from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE)
    has_read = models.BooleanField(_('has read'), default=False)
    content = models.TextField(_('content'))
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'message'
        verbose_name_plural = 'messages'

# class UnreadMessageCounter(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE)
#     unread_count = models.IntegerField(_('number of unread messages'), default=0)
