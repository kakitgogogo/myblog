from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponseRedirect, HttpResponse

from .models import Message

# Create your views here.

class MessageView(ListView):
    model = Message
    template_name = 'message/index.html'
    context_object_name = 'message_list'

    paginate_by = 20

    unread_count = 0

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponse(status=403) 
        self.unread_count = self.request.user.unread_message_count
        if self.unread_count > self.paginate_by:
            self.paginate_by = self.unread_count
        self.request.user.unread_message_count = 0
        self.request.user.save()
        return super(MessageView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        q = super(MessageView, self).get_queryset().filter(user=self.request.user)
        unread_list = q.filter(has_read=False)
        for item in unread_list:
            item.has_read = True
            item.save()
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        newdata = {
            'unread_count': self.unread_count
        }
        context.update(newdata)

        return context
    