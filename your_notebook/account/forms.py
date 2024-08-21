from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'ember-text-field ember-view sign-form__input'}),
            'password': forms.PasswordInput(attrs={'class': 'ember-text-field ember-view sign-form__input'}),
        }


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'ember-text-field ember-view st-input st-input_width_max st-size-normal'}),
            'last_name': forms.TextInput(attrs={'class':'ember-text-field ember-view st-input st-input_width_max st-size-normal'})
        }

class RegisterForm(UserCreationForm):
    policy = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-checkbox-class'
        }),
        required=True
    )
    class Meta:
        model = User
        fields = ('username',  'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'ember-text-field ember-view sign-form__input',
                'placeholder': 'Username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'ember-text-field ember-view sign-form__input',
                'placeholder': 'Email',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'ember-text-field ember-view sign-form__input',
                'placeholder': 'Password',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'ember-text-field ember-view sign-form__input',
                'placeholder': 'Confirm Password',
            })
        }