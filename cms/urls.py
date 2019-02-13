"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from . import views

# 设置命名空间
app_name = 'cms'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.log_out, name='log_out'),
    path('register', views.RegisterView2.as_view(), name='register'),
    path('img_captcha', views.img_captcha, name='img_captcha'),
    path('sms_captcha', views.send_sms_captcha, name='sms_captcha'),
    path('edit_account', views.edit_account, name='edit_account'),
    path('update', views.update_account, name='update_account'),
    path('update_password', views.UpdatePassword.as_view(), name='update_password'),
    path('send_emails', views.send_emails, name='send_emails'),
]
