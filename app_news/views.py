from django.contrib.auth import authenticate, login
from django.contrib.auth import views
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.core.exceptions import PermissionDenied
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


class LoginView(View):
    def get(self, request):
        form = AuthForm()
        return render(request, 'news/login.html', context={'form': form})

    def post(self, request):
        form = AuthForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_superuser:
                    if user.is_active:
                        login(request, user)
                        return redirect('/')
                    else:
                        form.add_error('__all__', 'Пользователь в бане!')
                else:
                    form.add_error('__all__', 'Ты админ)0)0))')
            else:
                form.add_error('__all__', 'Неверные данные!')
        return render(request, 'news/login.html', context={'form': form})


class LogoutView(views.LogoutView):
    next_page = '../'


class NewsListView(View):
    def get(self, request, *args, **kwargs):
        news = None
        if request.user.has_perm('app_news.publish_news'):
            news = News.objects.order_by('-created_at')
        else:
            news = News.objects.filter(confirmed=True).order_by('-created_at')
        form = FilterForm()

        tag_name = request.GET.get("filter_by")
        if tag_name and tag_name !='Все новости':
            tag = Tag.objects.filter(name=tag_name)[0]

            news = tag.news.all()

        return render(request, 'news/news.html', context={'form': form, 'news_list': news})


class UserDetailView(DetailView):
    model = Profile
    template_name = 'news/user_info.html'
    context_object_name = 'profile'
    slug_field = 'slug'


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = super(NewsDetailView, self).get_object()
        context['comments'] = Comment.objects.filter(news=obj).order_by('-id')
        if self.request.method == 'POST':
            context['form'] = AddCommentForm(self.request.POST)
        else:
            context['form'] = AddCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'publish' in request.POST:
            news = self.get_object()
            news.confirmed = True
            news.save()
        elif 'add_comment' in request.POST:
            form = AddCommentForm(request.POST)
            if form.is_valid():
                form.save()
                Comment.objects.create(**form.cleaned_data)
                comment = Comment.objects.last()
                news = self.get_object()
                comment.news = news
                if isinstance(request.user, User):
                    comment.author = request.user
                else:
                    user = None
                comment.save()

        return redirect(request.path)


class NewsCreateView(CreateView):
    model = News
    template_name = 'news/add_news.html'
    fields = ['title', 'content']

    context_object_name = 'form'
    success_url = '../'

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user)[0]
        profile.news_count += 1
        profile.save()
        return super(NewsCreateView, self).post(request, *args, **kwargs)


class VerifyFormView(View):
    def get(self, request):
        if not request.user.has_perm('app_news.view_profile'):
            raise PermissionDenied

        users = [user for user in User.objects.all()
                 if not user.groups.filter(name='Модераторы').exists()
                 and not user.is_superuser]
        form = VerifyForm()
        return render(request, 'news/verify_user.html',
                      context={'form': form, 'user_list': users})

    def post(self, request):
        users = [user for user in User.objects.all()
                 if not user.groups.filter(name='Модераторы').exists()
                 and not user.is_superuser]
        form = VerifyForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            verify = form.cleaned_data['verify']

            user = User.objects.filter(username=username).first()
            if user in users:
                user.profile.is_verified = verify
                group = Group.objects.get(name='Верифицированные')
                if verify:
                    group.user_set.add(user)
                else:
                    group.user_set.remove(user)
                group.save()
                user.profile.save()
                user.save()
            else:
                form.add_error('__all__', 'Такого пользователя нет')
        return render(request, 'news/verify_user.html',
                      context={'form': form, 'user_list': users})
