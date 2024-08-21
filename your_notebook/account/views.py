from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from account.forms import LoginForm, ProfileForm, RegisterForm
from account.models import User
from django_email_verification import send_email



class CustomLoginView(LoginView):
    template_name = 'account/login/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('account:profile')

    def get_success_url(self):
        return self.success_url


def logout_user(request):
    logout(request)
    return redirect('notebook:index')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'account/profile/profile_main.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid() and form.cleaned_data.get('policy'):
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f'Account created for {username}')
            # send_email(user)
            # return redirect('/account/email-verification-sent/')
            return redirect('account:login')
        else:
            print(form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        form = RegisterForm()
    return render(request, 'account/register/register.html', {"form": form})