"""djangoProject_PES URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.shortcuts import HttpResponse, render, redirect
from app01 import views


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'adminindex/', views.adminindex),   # 管理员登录界面
    path(r'teacherindex/', views.teacherindex),    # 教师登录界面
    path(r'studentindex/', views.studentindex),    # 学生登录界面
    path(r'index/', views.index),     # 登录
    path(r'logout/', views.logout),   # 登出
    path(r'view_score/', views.view_score),
    path(r'view_detail/', views.view_detail),
    path(r'view_evaluation/', views.view_evaluation),
    path(r'add_remove_user/', views.add_remove_user),
    path(r'change_permission/', views.change_permission),
    path(r'self_predict/',views.self_predict),
    path(r'update_detail/',views.update_detail),
    path(r'download/',views.download),
    path(r'update_system/',views.update_system),
    path(r'comment_detail/',views.comment_detail),
    path(r'update_password/',views.update_password)

]
