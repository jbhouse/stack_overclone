from django.conf.urls import url
from . import views

app_name = 'comments'

urlpatterns = [
    url(r'^answer/delete/(?P<pk>\d+)/$',views.DeleteAnswerComment,name='delete_answer_comment'),
    url(r'^question/delete/(?P<pk>\d+)/$',views.DeleteQuestionComment,name='delete_question_comment'),
    url(r'^question/create/(?P<pk>\d+)/$',views.CreateQuestionComment,name='create_question_comment'),
    url(r'^answer/create/(?P<pk>\d+)/$',views.CreateAnswerComment,name='create_answer_comment'),
]
