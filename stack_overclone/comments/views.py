from django.shortcuts import render
from django.views import generic
from answers.models import Answer
from questions.models import Question
from comments.models import AnswerComment,QuestionComment
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from comments.forms import AnswerCommentForm,QuestionCommentForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
def DeleteAnswerComment(request, **kwargs):
    answer_comment = get_object_or_404(AnswerComment, pk=kwargs['pk'])
    redirect_pk = answer_comment.answer.question.pk
    answer_comment.delete()
    return redirect('questions:detail', redirect_pk)

def DeleteQuestionComment(request, **kwargs):
    question_comment = get_object_or_404(QuestionComment, pk=kwargs['pk'])
    redirect_pk = question_comment.question.pk
    question_comment.delete()
    return redirect('questions:detail', redirect_pk)

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
        response_data = {}
        if request.user.is_authenticated():
            user = request.user
        question = get_object_or_404(Question, pk=kwargs['pk'])
        comment_text = request.POST.get('the_data')
        new_question_comment = QuestionComment.objects.create_question_comment(user, question)
        new_question_comment.text = comment_text
        new_question_comment.save()
        response_data['text'] = new_question_comment.text
        response_data['pk'] = kwargs['pk']
        print('-'*50)
        print(response_data)
        print('-'*50)
        # question_comment = QuestionCommentForm(request.POST)
        # if question_comment.is_valid():
        #     questioncomment = question_comment.save(commit=False)
        #     questioncomment.question = question
        #     questioncomment.user_id = request.user.id
        #     questioncomment.save()
    return JsonResponse(response_data)
