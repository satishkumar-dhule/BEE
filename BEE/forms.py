from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='email Required', widget=forms.TextInput(
        attrs={
        'class':'form-control input-sm',
        'placeholder':'email',
            "readonly":"true"
        }
    ))
    username = forms.CharField(max_length=200, help_text='username Required', widget=forms.TextInput(
        attrs={
        'class':'form-control input-sm',
        'placeholder':'username',
            "readonly": "true"
        }
    ))
    managerEmail = forms.EmailField(max_length=200, help_text='managerEmail Required', widget=forms.HiddenInput(
        attrs={
            "readonly": "true"
        }
    ))
    fullname = forms.CharField(max_length=200, help_text='fullname Required', widget=forms.HiddenInput(
        attrs={
            "readonly": "true"
        }
    ))
    managerName = forms.CharField(max_length=200, help_text='managerName Required', widget=forms.HiddenInput(
        attrs={
            "readonly": "true"
        }
    ))
    password2 = forms.CharField(max_length=200,help_text='password2 Required', widget=forms.PasswordInput(
        attrs={
        'class':'form-control input-sm',
        'placeholder':'password'
        }
    ))
    password1 = forms.CharField(max_length=200, help_text='password1 Required', widget=forms.PasswordInput(
        attrs={
        'class':'form-control input-sm',
        'placeholder':'password'
        }
    ))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','managerName','fullname','managerEmail')