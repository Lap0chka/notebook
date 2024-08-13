from django.contrib.auth.views import LoginView
from django.shortcuts import render

from account.forms import LoginForm


class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = LoginForm
