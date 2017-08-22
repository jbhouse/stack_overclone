from django.db import models
from django.contrib.auth import get_user_model
from questions.models import Question
from answers.models import Answer
User = get_user_model()
from django import template
register = template.Library()

class QuestionCommentManager(models.Manager):
    def create_question_comment(self, user, question):
        comment = self.create(user = user, question = question)
        return comment

class AnswerCommentManager(models.Manager):
    def create_answer_comment(self, user, answer):
        comment = self.create(user = user, answer = answer)
        return comment

class AnswerComment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User,related_name='users_answer_comment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    answer = models.ForeignKey(Answer, related_name='answer_comment', on_delete=models.CASCADE)
    objects = AnswerCommentManager()

    def __str__(self):
        return self.text

    class Meta:
        order_with_respect_to = 'answer'

class QuestionComment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User,related_name='users_question_comment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, related_name='question_comment', on_delete=models.CASCADE)
    objects = QuestionCommentManager()

    def __str__(self):
        return self.text

    class Meta:
        order_with_respect_to = 'question'
