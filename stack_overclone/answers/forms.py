from django.forms import ModelForm
from questions.models import Question
from answers.models import Answer

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['text'].label = 'Your Answer'
