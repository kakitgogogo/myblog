from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.conf import settings
from django.urls import reverse
from django.utils.html import strip_tags

import markdown

# Create your models here.

class Category(models.Model):
    name = models.CharField(_('category name'), max_length=50, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(_('tag name'),max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True, blank=False)
    body = models.TextField(_('body'))
    # excerpt = models.CharField(_('excerpt'), max_length=200, blank=True)

    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    modified_time = models.DateTimeField(_('last modified time'), auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'), on_delete=models.CASCADE)

    category = models.ForeignKey(Category, verbose_name=_('category'), on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name=_('tag'), blank=True)

    views = models.PositiveIntegerField(_('page views'), default=0)

    ACCESS_LEVEL_CHOICES = (
        ('public', 'public post'),
        ('private', 'private post'),
        ('protected', 'require password'),
    )
    access_level = models.CharField(
        _('access level'), 
        max_length=10, 
        choices=ACCESS_LEVEL_CHOICES, 
        default='public')
    password = models.CharField(_('password'), max_length=128, blank=True)

    sticky = models.BooleanField(_('sticky'), default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-sticky', '-created_time', '-id']
        verbose_name = 'post'
        verbose_name_plural = 'posts'
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # if not self.excerpt:
        #     md = markdown.Markdown(extensions=[
        #         'markdown.extensions.extra',
        #         'markdown.extensions.codehilite',
        #     ])
        #     self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)

