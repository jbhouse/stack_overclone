from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.urls import reverse
from django.http import HttpResponseForbidden
from . import forms
from questions.forms import QuestionForm
from comments.forms import AnswerCommentForm,QuestionCommentForm
from tags.forms import SelectTagForm
from answers.forms import AnswerForm
from django.views import generic
from questions.models import Question
from tags.models import Tag
from votes.models import QuestionVote
from answers.models import Answer
from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib.auth import get_user_model
User = get_user_model()

class CreateQuestion(generic.TemplateView,SelectRelatedMixin,LoginRequiredMixin):
    template_name = "questions/create_question.html"

    def get(self, request, *args, **kwargs):
        question_form = QuestionForm(self.request.GET or None)
        select_tag_form = SelectTagForm(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['question_form'] = question_form
        context['select_tag_form'] = select_tag_form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        def add_tag_to_question(request):
            questionform = QuestionForm(request.POST)
            if questionform.is_valid():
                question = questionform.save(commit=False)
                question.user_id = request.user.id
                question.save()
            tagform = SelectTagForm(request.POST)
            if tagform.is_valid():
                tags = tagform.cleaned_data.get('Tags')
                for tag_instance in tags:
                    tag = get_object_or_404(Tag, pk=int(tag_instance))
                    tag.question.add(question)
                    tag.save()
        view = add_tag_to_question(request)
        return redirect('questions:list')


class QuestionList(generic.ListView):
    model = Question
    template_name = 'questions/list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['question_list'] = super().get_queryset().order_by('-created_at')
        return context

class DeleteQuestion(LoginRequiredMixin,generic.DeleteView):
    model = Question
    success_url = reverse_lazy('questions:list')

class UserQuestions(generic.ListView):
    model = Question
    template_name = "questions/user_questions.html"

    def get_queryset(self):
        try:
            self.question_user = User.objects.prefetch_related("questions").get(username__iexact=self.request.user.username)
        except User.DoesNotExist:
            raise Http404
        else:
            return self.question_user.questions.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_questions"] = self.question_user.questions.all().order_by('-created_at')
        return context

class QuestionDetail(View):

    def get(self, request, *args, **kwargs):
        view = QuestionDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        def add_answer_to_question(request, pk):
            question = get_object_or_404(Question, pk=pk)
            if request.method == "POST":
                form = AnswerForm(request.POST)
                if form.is_valid():
                    answer = form.save(commit=False)
                    answer.question = question
                    answer.user_id = request.user.id
                    answer.save()
        view = add_answer_to_question(request, pk)
        return redirect('questions:detail', pk=kwargs['pk'])

class QuestionDisplay(generic.DetailView):
    model = Question
    template_name = 'questions/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDisplay, self).get_context_data(**kwargs)
        Q = get_object_or_404(Question, pk=self.kwargs['pk'])
        self.questions_tags = Tag.objects.prefetch_related("question").filter(question=Q)
        self.questions_comments = Question.objects.prefetch_related("question_comment").get(id=Q.pk)
        context['answer_form'] = AnswerForm()
        context['answer_comment_form'] = AnswerCommentForm()
        context['question_comment_form'] = QuestionCommentForm()
        context['questionstags'] = self.questions_tags
        context['question_comments'] = self.questions_comments.question_comment.all()
        return context

def UpVoteQuestion(request, **kwargs):
    # grab our question instance
    question = get_object_or_404(Question, pk=kwargs['pk'])
    # check for a validated user
    if request.user.is_authenticated():
        user = request.user
    # get all question votes this user has made
    users_question_votes = User.objects.prefetch_related('user_question_vote').get(username__iexact=request.user.username)
    # check if the user has voted on this question
    if users_question_votes.user_question_vote.all().filter(question = question).exists():
        # if it does, we set it equal to a nicely named variable
        user_vote_for_this_question = users_question_votes.user_question_vote.all().filter(question = question).get()
        # if the user has upvoted this question
        if user_vote_for_this_question.upvote == True:
            # we return the view with a message that you can only upvote once
            return redirect('questions:detail', pk=kwargs['pk'])
        # if the user has downvoted this question
        if user_vote_for_this_question.downvote == True:
            # we set downvote to false and upvote to true
            user_vote_for_this_question.upvote = True
            user_vote_for_this_question.downvote = False
            # we save this change in state!!!!!!!
            user_vote_for_this_question.save()
            question.votes += 2
            question.save()
            return redirect('questions:detail', pk=kwargs['pk'])
    # if they haven't voted on the question yet
    # create a new vote for this question, linked to this user
    new_question_vote = QuestionVote.objects.create_question_vote(user, question)
    new_question_vote.upvote = True
    new_question_vote.save()
    question.votes += 1
    question.save()
    return redirect('questions:detail', pk=kwargs['pk'])

def DownVoteQuestion(request, **kwargs):
    question = get_object_or_404(Question, pk=kwargs['pk'])
    if request.user.is_authenticated():
        user = request.user
    users_question_votes = User.objects.prefetch_related('user_question_vote').get(username__iexact=request.user.username)
    if users_question_votes.user_question_vote.all().filter(question = question).exists():
        user_vote_for_this_question = users_question_votes.user_question_vote.all().filter(question = question).get()
        if user_vote_for_this_question.downvote == True:
            return redirect('questions:detail', pk=kwargs['pk'])
        if user_vote_for_this_question.upvote == True:
            user_vote_for_this_question.downvote = True
            user_vote_for_this_question.upvote = False
            user_vote_for_this_question.save()
            question.votes -= 2
            question.save()
            return redirect('questions:detail', pk=kwargs['pk'])
    new_question_vote = QuestionVote.objects.create_question_vote(user, question)
    new_question_vote.downvote = True
    new_question_vote.save()
    question.votes -= 1
    question.save()
    return redirect('questions:detail', pk=kwargs['pk'])
