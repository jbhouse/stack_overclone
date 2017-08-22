from django.forms import ModelForm
from django import forms
from comments.models import AnswerComment,QuestionComment

class AnswerCommentForm(ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'id': 'answer-comment','class':'form-control','placeholder':'comment'}))
    class Meta:
        model = AnswerComment
        fields = ['text']


class QuestionCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'id': 'question-comment','class':'form-control','placeholder':'comment'}))
    class Meta:
        model = QuestionComment
        fields = ['text']
