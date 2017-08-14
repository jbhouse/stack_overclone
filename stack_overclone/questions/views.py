from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.urls import reverse
from django.http import HttpResponseForbidden
from . import forms
from questions.forms import QuestionForm
from answers.forms import AnswerForm
from django.views import generic
from questions.models import Question
from answers.models import Answer
from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib.auth import get_user_model
User = get_user_model()

class CreateQuestion(generic.CreateView,SelectRelatedMixin,LoginRequiredMixin):
    form_class = forms.QuestionForm
    success_url = reverse_lazy("questions:list")
    template_name = "questions/create_question.html"

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id
        self.object.save()
        return super().form_valid(form)

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
        view = add_answer_to_question(request, pk)
        return redirect('questions:detail', pk=kwargs['pk'])

class Answer(SingleObjectMixin, FormView):
    template_name = 'questions/question_detail.html'
    form_class = AnswerForm
    model = Answer

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super(Answer, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('questions:detail', kwargs={'pk': self.instance.pk})

class QuestionDisplay(generic.DetailView):
    model = Question
    template_name = 'questions/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDisplay, self).get_context_data(**kwargs)
        context['form'] = AnswerForm()
        return context

def add_answer_to_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user_id = request.user.id
            answer.save()
            return redirect('questions:detail', pk=question.pk)
    else:
        form = AnswerForm()
    return render(request, 'answers/_answer_form.html', {'form': form})
