from django.shortcuts import render
from . import forms
from private_messages.forms import MessageForm
from django.views import generic
from private_messages.models import PrivateMessage
from django.contrib.auth import get_user_model
User = get_user_model()
from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class CreateMessage(generic.CreateView,SelectRelatedMixin):
    form_class = forms.MessageForm
    success_url = reverse_lazy("home")
    template_name = "private_messages/new_message.html"


class MessageList(generic.ListView):
    model = PrivateMessage

class MessageDetail(SelectRelatedMixin,generic.DetailView):
    model = PrivateMessage
