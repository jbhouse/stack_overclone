from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from questions.models import Question
User = get_user_model()
from django import template
register = template.Library()

class AnswerManager(models.Manager):
    def create_answer(self, user, question):
        answer = self.create(user = user, question = question)
        return answer

class Answer(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User,related_name='answers')
    created_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    objects = AnswerManager()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("answers:detail")

    class Meta:
        order_with_respect_to = 'question'
