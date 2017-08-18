from django.db import models
from django.contrib.auth import get_user_model
from questions.models import Question
from answers.models import Answer
User = get_user_model()
from django import template
register = template.Library()


class AnswerComment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User,related_name='users_answer_comment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    answer = models.ForeignKey(Answer, related_name='answer_comment', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        order_with_respect_to = 'answer'

class QuestionComment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User,related_name='users_question_comment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, related_name='question_comment', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        order_with_respect_to = 'question'
