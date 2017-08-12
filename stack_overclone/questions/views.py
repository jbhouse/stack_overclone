from django.shortcuts import render
from . import forms
from questions.forms import QuestionForm
from django.views import generic
from questions.models import Question
from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib.auth import get_user_model
User = get_user_model()

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
    model = Question
    template_name = 'questions/list.html'

class DeleteQuestion(LoginRequiredMixin,generic.DeleteView):
    model = Question
    success_url = reverse_lazy('questions:list')

class QuestionDetail(generic.DetailView):
    model = Question

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
