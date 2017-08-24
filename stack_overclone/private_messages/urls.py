from django.conf.urls import url
from . import views

app_name = 'private_messages'

urlpatterns = [
    url(r'^$',views.PrivateMessageList.as_view(),name='list'),
    url(r'^new/$',views.CreatePrivateMessage,name='new_message'),
    url(r'^details/(?P<pk>\d+)/$',views.PrivateMessageDetail.as_view(),name='detail'),
    url(r'^delete/(?P<pk>\d+)/$',views.DeletePrivateMessage,name='delete'),
]
