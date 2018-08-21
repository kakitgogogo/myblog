from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from comments.models import Comment
from .models import Message
from users.models import BlogUser

class UnreadMessageCounterController:
    def __init__(self, user, *args, **kwargs):
        self.counter = user

    def update_unread_count(self, cnt):
        self.counter.unread_message_count += cnt
        self.counter.save()

    def mark_read(self, message_id):
        message = Message.objects.select_for_update().get(pk=message_id)
        if message.has_read:
            return
        message.has_read = True
        message.save()
        self.update_unread_count(-1)

@receiver(post_save, sender=Message)
def increase_unread_count_callback(sender, created, instance, **kwargs):
    if not created or instance.has_read:
        return
    UnreadMessageCounterController(instance.user).update_unread_count(1)

@receiver(post_delete, sender=Message)
def decrease_unread_count_callback(sender, instance, **kwargs):
    if not instance.has_read:
        UnreadMessageCounterController(instance.user).update_unread_count(-1)

@receiver(post_save, sender=Comment)
def comment_create_callback(sender, created, instance, **kwargs):
    if not created:
        return
    user = None
    content = None
    if instance.superior:
        user = instance.superior.author
        content = '''
        您在文章<a href="%s#comment-area" rel="bookmark" target="_blank">《%s》</a>中的评论有新回复
        '''% (instance.post.get_absolute_url(), instance.post.title)
    else:
        user = instance.post.author
        content = '''
        您的文章<a href="%s#comment-area" rel="bookmark" target="_blank">《%s》</a>有新评论
        '''% (instance.post.get_absolute_url(), instance.post.title)
    if instance.author.pk == user.pk:
        return
    message = Message(user=user, has_read=False, content=content)
    message.save()
    