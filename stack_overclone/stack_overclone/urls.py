"""stack_overclone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$',views.HomePage.as_view(),name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^tags/',include('tags.urls',namespace='tags')),
    url(r'^comments/',include('comments.urls',namespace='comments')),
    url(r'^questions/',include('questions.urls',namespace='questions')),
    url(r'^answers/',include('answers.urls',namespace='answers')),
    url(r'^messages/',include('private_messages.urls',namespace='private_messages')),
    url(r'^accounts/',include('accounts.urls',namespace='accounts')),
    url(r'^accounts/',include('django.contrib.auth.urls')),
    url(r'^login/$', views.LoginPage.as_view(),name='login_page'),
    url(r'^logout/$', views.LogoutPage.as_view(),name='logout_page'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
