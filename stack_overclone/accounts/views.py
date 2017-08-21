from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView,DetailView
from django.shortcuts import get_object_or_404
from questions.models import Question
from answers.models import Answer
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import JsonResponse

from . import forms

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

class ProfileView(DetailView):
    model = User
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.question_user = User.objects.prefetch_related('questions').get(pk=kwargs['object'].id)
        self.answer_user = User.objects.prefetch_related('answers').get(pk=kwargs['object'].id)
        context["user_questions"] = self.question_user.questions.all().order_by('-created_at')
        context["user_answers"] = self.answer_user.answers.all().order_by('-created_at')
        return context
