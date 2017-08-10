from django.shortcuts import render
from django.views.generic import TemplateView

class HomePage(TemplateView):
    template_name = 'index.html'

class LoginPage(TemplateView):
    template_name = 'login_page.html'

class LogoutPage(TemplateView):
    template_name = 'logout_page.html'
