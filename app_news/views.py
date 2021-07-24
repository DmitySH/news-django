from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from app_news.forms import *
from app_news.models import *


class RegisterView(View):
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            city = form.cleaned_data.get('city')
            Profile.objects.create(
                user=user,
                city=city,
                phone_number=phone_number,
            )

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        return render(request, 'news/register.html', {'form': form})

    def get(self, request):
        form = RegisterForm()
        return render(request, 'news/register.html', {'form': form})
