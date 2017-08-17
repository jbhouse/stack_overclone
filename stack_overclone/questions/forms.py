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

# class QuestionVotes(ModelForm):
#     class Meta:
#         model = Question
#         fields = ['votes']
  # <div class="container">
  #     <form method="post">
  #         {% csrf_token %}
  #         {% bootstrap_form question_vote_form %}
  #         <input type="submit" value="Vote" class="btn btn-default">
  #     </form>
  # </div>
