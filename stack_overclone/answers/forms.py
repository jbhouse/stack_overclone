from django.forms import ModelForm
from django import forms
# from questions.models import Question
from answers.models import Answer

class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'id': 'answer','class':'form-control','placeholder':'comment'}))
    class Meta:
        model = Answer
        fields = ['text']
