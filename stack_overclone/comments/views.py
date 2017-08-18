from django.shortcuts import render
from django.views import generic
from answers.models import Answer
from questions.models import Question
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class DeleteAnswerComment(LoginRequiredMixin,generic.DeleteView):
    model = Answer
    success_url = reverse_lazy('questions:list')

class DeleteQuestionComment(LoginRequiredMixin,generic.DeleteView):
    model = Question
    success_url = reverse_lazy('questions:list')
