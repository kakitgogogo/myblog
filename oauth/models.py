from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Create your models here.

class OAuthUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='user', on_delete=models.CASCADE)
    userid = models.CharField(_('user id'), max_length=50, blank=False, null=False)
    platform = models.CharField(_('third party platform'), blank=False, null=False, max_length=50)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'OAuth Users'
