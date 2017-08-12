from django.shortcuts import render
from . import forms
from questions.forms import QuestionForm
from django.views import generic
from . import models
from questions.models import Question
from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

class CreateQuestion(generic.CreateView,SelectRelatedMixin,LoginRequiredMixin):
    form_class = forms.QuestionForm
    success_url = reverse_lazy("home")
    template_name = "questions/create_question.html"

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id
        self.object.save()
        return super().form_valid(form)

class QuestionList(generic.ListView):
    model = models.Question
    # select_related = ('user', 'question')
    template_name = 'questions/list.html'

class DeleteQuestion(LoginRequiredMixin,generic.DeleteView):
    model = Question
    success_url = reverse_lazy('questions:list')

class QuestionDetail(generic.DetailView):
    model = Question
