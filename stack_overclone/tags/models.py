from django.db import models
from django.core.urlresolvers import reverse
from questions.models import Question
from django import template
register = template.Library()
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=30)
    question = models.ManyToManyField(Question)

    def __str__(self):
        return self.name
