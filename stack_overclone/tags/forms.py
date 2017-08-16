from django.forms import ModelForm
from django import forms
from tags.models import Tag
from questions.models import Question

# class SelectTagForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(SelectTagForm, self).__init__(*args, **kwargs)
#         self.fields['options'].empty_label = None
#
#     class Meta:
#         model=Tag
#         fields=('Javascript','Ruby','Python','Node.js','Rails','Django','CSS','HTML')
#         widgets={'options': forms.CheckboxSelectMultiple()}

class SelectTagForm(forms.Form):

    OPTIONS = [
    ('0','Javascript'),
    ('1','Ruby'),
    ('2','Python'),
    ('3','Node.js'),
    ('4','Rails'),
    ('5','Django'),
    ('6','HTML'),
    ('7','CSS'),
    ]

    Tags = forms.MultipleChoiceField(
    choices=OPTIONS, widget=forms.CheckboxSelectMultiple(),
    label='Add a tag', required=True, error_messages={'required': 'tags are required'})
