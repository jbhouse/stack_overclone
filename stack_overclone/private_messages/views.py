from django.shortcuts import render
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
from django.http import Http404
# from django.shortcuts import get_object_or_404
from django.contrib import messages

# Create your views here.

class CreatePrivateMessage(generic.CreateView,SelectRelatedMixin,LoginRequiredMixin):
    form_class = forms.MessageForm
    success_url = reverse_lazy('private_messages:list')
    template_name = "private_messages/new_message.html"

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.sender_id = self.request.user.id
        self.object.save()
        return super().form_valid(form)

class PrivateMessageList(generic.ListView):
    model = models.PrivateMessage
    template_name = 'private_messages/privatemessage_list.html'

    def get_queryset(self):
        self.message_recipient = User.objects.prefetch_related('recipient').get(username__iexact=self.request.user.username)
        self.message_sender = User.objects.prefetch_related('sender').get(username__iexact=self.request.user.username)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['users_inbox'] = self.message_recipient.recipient.all().order_by('-created_at')
        context['users_outbox'] = self.message_sender.sender.all().order_by('-created_at')
        return context

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
