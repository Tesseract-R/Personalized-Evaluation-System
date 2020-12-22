from django.shortcuts import render, HttpResponse, redirect
from app01 import models
import pymysql

from django import forms
from django.forms import fields
from django.forms import widgets

import pymysql


# Create your views here.

class TestForm(forms.Form):
    user_id = fields.CharField(
        required=True,
        max_length=30,
        min_length=3,
        error_messages={"required": '不能为空'}, )

    user_name = fields.CharField(
        required=False,
        max_length=30,
        min_length=3,
        error_messages={"required": '不能为空'}, )

    user_type = fields.ChoiceField(
        choices=[('TEACHER', "老师"), ('TA', "助教"), ('STUDENT', "学生"), ('ADMIN', "管理员")],  # 单选下拉框
        initial='STUDENT'
    )


def adminindex(request, name):
    return render(request, 'adminindex.html', {'name': name})


def teacherindex(request, name):
    return render(request, 'teacherindex.html', {'name': name})


def studentindex(request, name):
    if name == 'newStudent':
        return render(request, 'studentindex.html',
                      {'name': name, 'structure_design': 'null', 'software_process': 'null',
                       'detailed_design': 'null', 'demand_analysis': 'null',
                       'realization': 'null', 'maintenance': 'null', 'final_score': 'null'})
        # return render(request,'predict_score.html',{'name':name})
    ret_name = models.User.objects.filter(userid=name)
    username = ret_name[0].username
    ret = models.result_store.objects.filter(userid=name)
    structure_design = ret[0].inclass_score1
    software_process = ret[0].inclass_score2
    detailed_design = ret[0].inclass_score3
    demand_analysis = ret[0].inclass_score4
    realization = ret[0].inclass_score5
    maintenance = ret[0].inclass_score6
    final_score = ret[0].final_score
    comment = ret[0].comment
    return render(request, 'studentindex.html',
                  {'name': username, 'structure_design': structure_design, 'software_process': software_process,
                   'detailed_design': detailed_design, 'demand_analysis': demand_analysis,
                   'realization': realization, 'maintenance': maintenance, 'final_score': final_score,
                   'comment': comment})


def index(request):
    # 返回结果
    error_msg = ""
    if request.method == "POST":
        user = request.POST['username']
        pwd = request.POST['password']
        if not models.User.objects.filter(userid=user):
            error_msg = "登录失败，该用户不存在！"
            return render(request, 'index.html', {"error": error_msg})

        ret = models.User.objects.filter(userid=user, password=pwd)
        if ret:  # 登陆成功
            if ret[0].usertype == 'ADMIN':  # 根据用户身份导向不同的页面
                return adminindex(request, user)
            elif ret[0].usertype == 'TEACHER' or ret[0].usertype == 'TA':
                return teacherindex(request, user)
            elif ret[0].usertype == 'STUDENT':
                return studentindex(request, user)
            else:
                return studentindex(request, 'newStudent')
        else:
            error_msg = "登录失败，请检查用户名和密码！"

    return render(request, 'index.html', {"error": error_msg})


def logout(request):
    return HttpResponse("登出成功！请关闭页面。")


def view_score(request):
    if request.method == "POST":
        user_id = request.POST['001']
        user_name = request.POST['002']
        if user_id == "":
            if not models.User.objects.filter(username=user_name):
                return render(request, 'view_score.html',
                              {'name': 'test', 'student_id': user_name, 'score': "该学生不存在！"})
            ret = models.User.objects.filter(username=user_name)
            user_id = ret[0].userid
        if not models.result_store.objects.filter(userid=user_id):
            return render(request, 'view_score.html',
                          {'name': 'test', 'student_id': user_name, 'score': "该学生不存在！"})
        else:
            ret = models.result_store.objects.filter(userid=user_id)
            ret_name = models.User.objects.filter(userid=user_id)
            user_name = ret_name[0].username
            return_value = ret[0].final_score
        return render(request, 'view_score.html',
                      {'name': 'test', 'student_id': user_name, 'score': return_value})
    return render(request, 'view_score.html', {'name': 'test'})


def add_remove_user(request):
    if request.method == "POST":
        if 'add' in request.POST:
            obj = TestForm(request.POST)
            user_id = obj.data['user_id']
            if models.User.objects.filter(userid=user_id):
                msg = "用户的学号已经存在！"
                return render(request, 'add_remove_user.html',
                              {"obj": obj, 'name': 'admin', 'student_id': user_id, 'msg': msg})
            else:
                user_name = obj.data['user_name']
                user_type = obj.data['user_type']
                models.User.objects.create(userid=user_id, username=user_name, password="123456", usertype=user_type)
                models.result_store.objects.create(userid=user_id, inclass_score1=0, inclass_score2=0, inclass_score3=0,
                                                   inclass_score4=0, inclass_score5=0, inclass_score6=0, final_score=0,
                                                   comment='default')
                msg = "创建成功"
                return render(request, 'add_remove_user.html',
                              {"obj": obj, 'name': 'admin', 'student_id': user_id, 'msg': msg, 'user_type':user_type})
        if 'delete' in request.POST:
            obj = TestForm(request.POST)
            user_id = obj.data['user_id']
            if user_id == 'admin':
                return render(request, 'add_remove_user.html',
                              {"obj": obj, 'name': 'admin', 'student_id': user_id, 'msg': "不允许删除超级管理员"})
            if not models.User.objects.filter(userid=user_id):
                msg = "待删除用户不存在！"
                return render(request, 'add_remove_user.html',
                              {"obj": obj, 'name': 'admin', 'student_id': user_id, 'msg': msg})
            else:
                q1 = models.User.objects.filter(userid=user_id).last()
                q1.delete()
                msg = "删除成功"
                return render(request, 'add_remove_user.html',
                              {"obj": obj, 'name': 'admin', 'student_id': user_id, 'msg': msg})
    obj = TestForm()
    return render(request, 'add_remove_user.html', {"obj": obj, 'name': 'admin'})


def change_permission(request):
    if request.method == "POST":
        obj = TestForm(request.POST)
        user_id = obj.data['user_id']
        if user_id == 'admin':
            return render(request, 'change_permission.html',
                          {"obj": obj, 'name': 'admin', 'user_id': user_id, 'msg': "不允许修改超级管理员权限！"})
        if not models.User.objects.filter(userid=user_id):
            msg = "用户不存在！"
            return render(request, 'change_permission.html',
                          {"obj": obj, 'name': 'admin', 'user_id': user_id, 'msg': msg})
        else:
            ret = models.User.objects.filter(userid=user_id)
            type_before = ret[0].usertype
            ret = models.User.objects.get(userid=user_id)
            type_after = obj.data['user_type']
            ret.usertype = type_after
            ret.save()
            msg = "修改权限成功"
            return render(request, 'change_permission.html',
                          {"obj": obj, 'name': 'admin', 'user_id': user_id, 'msg': msg,
                           'type_before': type_before, 'type_after': type_after})
    obj = TestForm()
    return render(request, 'change_permission.html', {"obj": obj, 'name': 'admin'})