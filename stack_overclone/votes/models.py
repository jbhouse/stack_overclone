from django.db import models
from questions.models import Question
from answers.models import Answer
from django.contrib.auth import get_user_model
User = get_user_model()
from django import template
register = template.Library()
# Create your models here.

class QuestionManager(models.Manager):
    def create_question_vote(self, user, question):
        question = self.create(user = user, question = question)
        return question

class AnswerManager(models.Manager):
    def create_answer_vote(self, user, answer):
        answer = self.create(user = user, answer = answer)
        return answer

class QuestionVote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_vote')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_question_vote')
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)
    objects = QuestionManager()


class AnswerVote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_vote')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answer_vote')
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)
    objects = AnswerManager()
