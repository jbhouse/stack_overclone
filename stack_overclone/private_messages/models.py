from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

class PrivateMessageManager(models.Manager):
    def create_private_message(self, sender, recipient):
        private_message = self.create(sender = sender, recipient = recipient)
        return private_message

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sender")
    recipient = models.ForeignKey(User, related_name="recipient")
    subject = models.CharField(max_length=256,unique=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    objects = PrivateMessageManager()

    def __str__(self):
        return self.subject
