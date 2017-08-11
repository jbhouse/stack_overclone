from django.conf.urls import url
from . import views

app_name = 'private_messages'

urlpatterns = [
    url(r'^$',views.MessageList.as_view(),name='list'),
    url(r'^new/$', views.CreateMessage.as_view(),name='new_message'),
]
