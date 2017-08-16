from django.forms import ModelForm
from django import forms
from tags.models import Tag
from questions.models import Question

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
