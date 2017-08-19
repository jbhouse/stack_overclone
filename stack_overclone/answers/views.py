from django.shortcuts import render
from . import forms
from answers.forms import AnswerForm
from django.views import generic
from answers.models import Answer
from questions.models import Question
from django.shortcuts import redirect
from votes.models import AnswerVote
from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model
User = get_user_model()

class DeleteAnswer(LoginRequiredMixin,generic.DeleteView):
    model = Answer

    success_url = reverse_lazy('questions:list')

class UserAnswers(generic.ListView):
    model = Answer
    template_name = "answers/user_answers.html"

    def get_queryset(self):
        try:
            self.answer_user = User.objects.prefetch_related('questions').get(username__iexact=self.request.user.username)
        except User.DoesNotExist:
            raise Http404
        else:
            return self.answer_user.answers.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_answers"] = self.answer_user.answers.all().order_by('-created_at')
        return context

def UpVoteAnswer(request, **kwargs):
    answer = get_object_or_404(Answer, pk=kwargs['pk'])
    if request.user.is_authenticated():
        user = request.user
    users_answer_votes = User.objects.prefetch_related('user_answer_vote').get(username__iexact=request.user.username)
    if users_answer_votes.user_answer_vote.all().filter(answer = answer).exists():
        user_vote_for_this_answer = users_answer_votes.user_answer_vote.all().filter(answer = answer).get()
        if user_vote_for_this_answer.upvote == True:
            return redirect('questions:detail', pk=answer.question.pk)
        if user_vote_for_this_answer.downvote == True:
            user_vote_for_this_answer.upvote = True
            user_vote_for_this_answer.downvote = False
            user_vote_for_this_answer.save()
            answer.votes += 2
            answer.save()
            return redirect('questions:detail', pk=answer.question.pk)
    new_answer_vote = AnswerVote.objects.create_answer_vote(user, answer)
    new_answer_vote.upvote = True
    new_answer_vote.save()
    answer.votes += 1
    answer.save()
    return redirect('questions:detail', pk=answer.question.pk)

def DownVoteAnswer(request, **kwargs):
    answer = get_object_or_404(Answer, pk=kwargs['pk'])
    if request.user.is_authenticated():
        user = request.user
    users_answer_votes = User.objects.prefetch_related('user_answer_vote').get(username__iexact=request.user.username)
    if users_answer_votes.user_answer_vote.all().filter(answer = answer).exists():
        user_vote_for_this_answer = users_answer_votes.user_answer_vote.all().filter(answer = answer).get()
        if user_vote_for_this_answer.downvote == True:
            return redirect('questions:detail', pk=answer.question.pk)
        if user_vote_for_this_answer.upvote == True:
            user_vote_for_this_answer.downvote = True
            user_vote_for_this_answer.upvote = False
            user_vote_for_this_answer.save()
            answer.votes -= 2
            answer.save()
            return redirect('questions:detail', pk=answer.question.pk)
    new_answer_vote = AnswerVote.objects.create_answer_vote(user, answer)
    new_answer_vote.downvote = True
    new_answer_vote.save()
    answer.votes -= 1
    answer.save()
    return redirect('questions:detail', pk=answer.question.pk)
