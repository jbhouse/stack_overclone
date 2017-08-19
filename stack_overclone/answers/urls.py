from django.conf.urls import url
from . import views

app_name = 'answers'

urlpatterns = [
    url(r'^upvote/(?P<pk>\d+)/$',views.UpVoteAnswer,name='upvote'),
    url(r'^downvote/(?P<pk>\d+)/$',views.DownVoteAnswer,name='downvote'),
    # url(r'^view/(?P<pk>\d+)/$',views.AnswerDetail.as_view(),name='detail'),
    url(r'^delete/(?P<pk>\d+)/$',views.DeleteAnswer.as_view(),name='delete'),
    url(r"^by/(?P<username>[-\w]+)/$",views.UserAnswers.as_view(),name="by_user"),
]
