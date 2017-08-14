from django.shortcuts import render
from . import forms
from answers.forms import AnswerForm
from django.views import generic
from answers.models import Answer
from questions.models import Question
from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib.auth import get_user_model
User = get_user_model()

# class CreateAnswer(generic.CreateView,SelectRelatedMixin,LoginRequiredMixin):
#     form_class = forms.AnswerForm
#     success_url = reverse_lazy("questions:detail" pk=question.pk)
#     template_name = "questions/create_answer.html"
#
#     def form_valid(self,form):
#         self.object = form.save(commit=False)
#         self.object.user_id = self.request.user.id
#         self.object.save()
#         return super().form_valid(form)

# class AnswerList(generic.ListView):
#     model = Answer
#     template_name = 'answers/list.html'

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['question_list'] = super().get_queryset().order_by('-created_at')
    #     return context

class DeleteAnswer(LoginRequiredMixin,generic.DeleteView):
    model = Answer
    success_url = reverse_lazy('questions:list')

class AnswerDetail(generic.DetailView):
    model = Question

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
