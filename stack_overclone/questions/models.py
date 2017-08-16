from django.db import models
import misaka
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from django import template
register = template.Library()

class Question(models.Model):
    title = models.CharField(max_length=256,unique=True)
    user = models.ForeignKey(User,related_name='questions')
    created_at = models.DateTimeField(auto_now=True)
    details = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("questions:detail", pk=self.pk)

    class Meta:
        ordering = ['created_at']
