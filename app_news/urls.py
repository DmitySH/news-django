from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', views.NewsListView.as_view(), name='news'),
    path('<slug:slug>/', views.UserDetailView.as_view(), name='user-info'),

]