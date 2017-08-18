from django.conf.urls import url
from . import views

app_name = 'comments'


urlpatterns = [
    url(r'^answer/delete/(?P<pk>\d+)/$',views.DeleteAnswerComment.as_view(),name='delete_answer_comment'),
    url(r'^question/delete/(?P<pk>\d+)/$',views.DeleteQuestionComment.as_view(),name='delete_question_comment'),
]
