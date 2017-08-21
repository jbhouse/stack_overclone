from django.forms import ModelForm
from questions.models import Question

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title','details']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['title'].label = 'Title'
        self.fields['details'].label = 'Details'
