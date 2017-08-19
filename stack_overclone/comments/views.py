from django.shortcuts import render
from django.views import generic
from answers.models import Answer
from questions.models import Question
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from comments.forms import AnswerCommentForm,QuestionCommentForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
# Create your views here.
class DeleteAnswerComment(LoginRequiredMixin,generic.DeleteView):
    model = Answer
    success_url = reverse_lazy('questions:list')

class DeleteQuestionComment(LoginRequiredMixin,generic.DeleteView):
    model = Question
    success_url = reverse_lazy('questions:list')

def CreateAnswerComment(request, **kwargs):
    if request.method == "POST":
        answer = get_object_or_404(Answer, pk=kwargs['pk'])
        answer_comment = AnswerCommentForm(request.POST)
        if answer_comment.is_valid():
            answercomment = answer_comment.save(commit=False)
            answercomment.answer = answer
            answercomment.user_id = request.user.id
            answercomment.save()
    return redirect('questions:detail', answer.question.pk)

def CreateQuestionComment(request, **kwargs):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=kwargs['pk'])
        question_comment = QuestionCommentForm(request.POST)
        if question_comment.is_valid():
            questioncomment = question_comment.save(commit=False)
            questioncomment.question = question
            questioncomment.user_id = request.user.id
            questioncomment.save()
    return redirect('questions:detail', pk=kwargs['pk'])
