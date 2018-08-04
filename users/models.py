from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.sites.models import Site
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.files.base import ContentFile

import uuid

from .randomavatar import Avatar
from .validators import UsernameValidator
# Create your models here.

class BlogUser(AbstractUser):
    username_validator = UsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and -/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    nickname = models.CharField(_('nickname'), max_length=100, blank=True)
    mugshot = models.ImageField(_('mugshot'), upload_to='images', blank=True)
    date_modified = models.DateTimeField(_('date modified'), default=now)
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True, error_messages={'unique':'The email address is already occupied'})

    class Meta(AbstractUser.Meta):
        pass

    def get_absolute_url(self):
        return ""
    
    def __str__(self):
        return self.username

    def get_full_url(self):
        site = Site.objects.get_current().domain
        return "http://{site}{path}".format(site=site, path=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        if self.nickname is None or self.nickname.strip() == '':
            self.nickname = self.username
        if not self.mugshot:
            avatar = Avatar(rows=10, columns=10)
            image_bytes = avatar.get_image(string=self.username,
                                                width=480,
                                                height=480,
                                                pad=10)
            filename = str(uuid.uuid4().hex) + '.png'
            self.mugshot.save(filename, ContentFile(image_bytes), save=False)

        super(BlogUser, self).save(*args, **kwargs)