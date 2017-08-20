from django.shortcuts import render
from django.views import generic
from tags.models import Tag
from questions.models import Question
from django.contrib.auth import get_user_model
User = get_user_model()

class TagQuestions(generic.DetailView):
    model = Tag
    template_name = "tags/tag_questions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.this_tags_questions = Tag.objects.prefetch_related('question').get(id=kwargs['object'].id)
        context["questions_list"] = self.this_tags_questions.question.all()
        return context

class TagList(generic.ListView):
    model = Tag
    template_name = "tags/tag_list.html"
