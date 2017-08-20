from django.conf.urls import url
from . import views

app_name = 'questions'

urlpatterns = [
    url(r'^new/$',views.CreateQuestion.as_view(),name='new_question'),
    url(r'^all/$',views.QuestionList.as_view(),name='list'),
    url(r'^view/(?P<pk>\d+)/$',views.QuestionDetail.as_view(),name='detail'),
    url(r'^delete/(?P<pk>\d+)/$',views.DeleteQuestion,name='delete'),
    url(r'^upvote/(?P<pk>\d+)/$',views.UpVoteQuestion,name='upvote'),
    url(r'^downvote/(?P<pk>\d+)/$',views.DownVoteQuestion,name='downvote'),
    url(r"^by/(?P<username>[-\w]+)/$",views.UserQuestions.as_view(),name="by_user"),
]
