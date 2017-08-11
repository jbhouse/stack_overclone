from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sender")
    recipient = models.ForeignKey(User, related_name="recipient")
    subject = models.CharField(max_length=256,unique=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
