from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from app_news.models import *


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=False, help_text='Имя')
    last_name = forms.CharField(max_length=20, required=False, help_text='Фамилия')
    city = forms.CharField(max_length=36, required=False, help_text='Город')
    phone_number = forms.CharField(max_length=12, required=False,
                                   help_text='Номер телефона')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class VerifyForm(forms.Form):
    username = forms.CharField(help_text='Имя пользователя')
    verify = forms.BooleanField(widget=forms.CheckboxInput, required=False)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['news', 'author']


class FilterForm(forms.Form):
    FILTER_CHOICES = (
        (tag.name, tag.name) for tag in Tag.objects.all()
    )

    filter_by = forms.ChoiceField(choices=FILTER_CHOICES)
