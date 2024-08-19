from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from account.forms import LoginForm, ProfileForm


class CustomLoginView(LoginView):
    template_name = 'account/login.html'
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
