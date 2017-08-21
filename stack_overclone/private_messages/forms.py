from django.forms import ModelForm
from private_messages.models import PrivateMessage
from django import forms

class MessageForm(ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['recipient', 'subject', 'message']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['recipient'].label = 'Recipient'
        self.fields['subject'].label = 'Subject'
        self.fields['message'].label = 'Message'
