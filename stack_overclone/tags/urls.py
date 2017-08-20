from django.conf.urls import url
from . import views

app_name = 'tags'

urlpatterns = [
    url(r'^questions/(?P<pk>\d+)/$',views.TagQuestions.as_view(),name='detail'),
    url(r'^list/$',views.TagList.as_view(),name='list')
]
