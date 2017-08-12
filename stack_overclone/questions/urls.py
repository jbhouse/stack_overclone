from django.conf.urls import url
from . import views

app_name = 'questions'

urlpatterns = [
    url(r'^new/$',views.CreateQuestion.as_view(),name='new_question'),
    url(r'^all/$',views.QuestionList.as_view(),name='list'),
    url(r'^view/(?P<pk>\d+)/$',views.QuestionDetail.as_view(),name='detail'),
    url(r'^delete/(?P<pk>\d+)/$',views.DeleteQuestion.as_view(),name='delete'),
    url(r"by/(?P<username>[-\w]+)/$",views.UserQuestions.as_view(),name="by_user"),
]
