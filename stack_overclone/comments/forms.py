from django.forms import ModelForm
from django import forms
from comments.models import AnswerComment,QuestionComment

class AnswerCommentForm(ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'comment'}))
    class Meta:
        model = AnswerComment
        fields = ['text']

    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.fields['text'].label = 'Your Comment'

class QuestionCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'comment'}))
    class Meta:
        model = QuestionComment
        fields = ['text']

    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.fields['text'].label = 'Your Comment'
