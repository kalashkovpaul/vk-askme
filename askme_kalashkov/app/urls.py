"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

app_urlpatterns = [
    path('question/', views.question, name="question"),
    path('question/2/', views.question),
    path('ask/', views.ask, name="ask"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('settings/', views.settings, name="settings"),
    path('tag/', views.tagged, name="tag"),
    path('tag/hoho/', views.tagged),
    path('profile/', views.profile, name="profile"),
    path('profile/User_666/', views.profile),
    path('hot/', views.hot, name="hot"),
]