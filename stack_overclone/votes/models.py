# from django.db import models
# from questions.models import Question
# from answers.models import Answer
# from django.contrib.auth import get_user_model
# User = get_user_model()
# from django import template
# register = template.Library()
# # Create your models here.
# class Vote(models.Model):
#     answer = models.ForeignKey(Answer, blank=True, null=True, on_delete=models.CASCADE, related_name='vote_answer')
#     question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE, related_name='vote_question')
#     user = models.ForeignKey(User, related_name='vote_user')
