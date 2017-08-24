from django.shortcuts import render
from django.shortcuts import redirect
from . import forms
from private_messages.forms import MessageForm
from django.views import generic
from . import models
from private_messages.models import PrivateMessage
from django.contrib.auth import get_user_model
User = get_user_model()
from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404,JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages

def CreatePrivateMessage(request):
    if request.method == "POST":
        response_data = {}
        if request.user.is_authenticated():
            sender = request.user
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        recipient_id = request.POST.get('recipient')
        recipient = get_object_or_404(User, pk=recipient_id)
        new_pm = PrivateMessage.objects.create_private_message(sender,recipient)
        new_pm.subject = subject
        new_pm.message = message
        new_pm.save()
        response_data['recipient_id'] = recipient_id
        response_data['sender_id'] = sender.pk
        response_data['message_pk'] = new_pm.pk
        response_data['message'] = new_pm.message
        response_data['subject'] = new_pm.subject
        response_data['username'] = new_pm.sender.username
        return JsonResponse(response_data)

class PrivateMessageList(generic.TemplateView,SelectRelatedMixin,LoginRequiredMixin):
    model = models.PrivateMessage
    template_name = 'private_messages/privatemessage_list.html'

    def get(self, request, *args, **kwargs):
        message_form = MessageForm(self.request.GET or None)
        message_recipient = User.objects.prefetch_related('recipient').get(username__iexact=self.request.user.username)
        message_sender = User.objects.prefetch_related('sender').get(username__iexact=self.request.user.username)
        context = self.get_context_data(**kwargs)
        context['message_form'] = message_form
        context['users_inbox'] = message_recipient.recipient.all().order_by('-created_at')
        context['users_outbox'] = message_sender.sender.all().order_by('-created_at')
        return self.render_to_response(context)

    # def get_queryset(self):
    #     self.message_recipient = User.objects.prefetch_related('recipient').get(username__iexact=self.request.user.username)
    #     self.message_sender = User.objects.prefetch_related('sender').get(username__iexact=self.request.user.username)
    #
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['users_inbox'] = self.message_recipient.recipient.all().order_by('-created_at')
    #     context['users_outbox'] = self.message_sender.sender.all().order_by('-created_at')
    #     return context

class PrivateMessageDetail(SelectRelatedMixin,generic.DetailView):
    model = PrivateMessage
    select_related = ('sender','recipient')

    def query_set(self):
        queryset = super().get_queryset()
        return queryset.filter(recipient = self.request.user)

class DeletePrivateMessage(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = PrivateMessage
    select_related = ('sender','recipient')
    success_url = reverse_lazy('private_messages:list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(recipient = self.request.user)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Message Deleted')
        return super().delete(*args,**kwargs)
