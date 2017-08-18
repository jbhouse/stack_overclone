from django.forms import ModelForm
from comments.models import AnswerComment,QuestionComment


class AnswerCommentForm(ModelForm):
    class Meta:
        model = AnswerComment
        fields = ['text']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['text'].label = 'Your Comment'

class QuestionCommentForm(ModelForm):
    class Meta:
        model = QuestionComment
        fields = ['text']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['text'].label = 'Your Comment'
