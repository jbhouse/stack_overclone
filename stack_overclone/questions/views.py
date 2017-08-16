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
from tags.forms import SelectTagForm
from answers.forms import AnswerForm
from django.views import generic
from questions.models import Question
from tags.models import Tag
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
            tag = get_object_or_404(Tag, pk=tags[0])
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

    # def get_queryset(self):
    # #     Q = get_object_or_404(Question, pk=self.kwargs['pk'])
    #     self.questions_tags = Tag.objects.prefetch_related("question")
    #     print('/'*50)
    #     print(self.questions_tags)
    #     print('/'*50)

    def get_context_data(self, **kwargs):
        context = super(QuestionDisplay, self).get_context_data(**kwargs)
        Q = get_object_or_404(Question, pk=self.kwargs['pk'])
        self.questions_tags = Tag.objects.prefetch_related("question").get(question=Q)
        print('/'*50)
        print(self.questions_tags)
        context['form'] = AnswerForm()
        print('/'*50)
        context['questionstags'] = self.questions_tags
        # print(context)
        return context
