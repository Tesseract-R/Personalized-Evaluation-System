import joblib
from django.shortcuts import render, HttpResponse, redirect
from app01 import models
import pymysql

from django import forms
from django.forms import fields
from django.forms import widgets

from sklearn.preprocessing import MinMaxScaler
import pymysql


# Create your views here.

class addForm(forms.Form):
    user_id = fields.CharField(
        label='学号/编号',
        required=True,
        max_length=30,
        min_length=3,
        error_messages={"required": '不能为空'})

    user_name = fields.CharField(
        label='用户名',
        required=False,
        max_length=30,
        min_length=3,
        error_messages={"required": '不能为空'}, )

    user_type = fields.ChoiceField(
        label='用户类型',
        choices=[('TEACHER', "老师"), ('TA', "助教"), ('STUDENT', "学生"), ('ADMIN', "管理员")],  # 单选下拉框
        initial='STUDENT'
    )

class deleteForm(forms.Form):
    user_id = fields.CharField(
        label='用户名',
        widget=widgets.Select())

    user_type = fields.ChoiceField(
        label='用户类型',
        choices=[('TEACHER', "老师"), ('TA', "助教"), ('STUDENT', "学生"), ('ADMIN', "管理员")],  # 单选下拉框
        initial='STUDENT')

    checkbox = fields.ChoiceField(
        required=True,
        label="确定删除",
        widget=forms.widgets.CheckboxInput()
    )

    def __init__(self,*args,**kwargs):
        super(deleteForm,self).__init__(*args,**kwargs)
        self.fields['user_id'].widget.choices=models.User.objects.values_list('userid','username')

class RequestForm(forms.Form):   # 这个是用于找所有学生信息的
    user_id = fields.CharField(
        label='学生学号',
        widget=widgets.Select())

    def __init__(self,*args,**kwargs):
        super(RequestForm,self).__init__(*args,**kwargs)
        self.fields['user_id'].widget.choices=models.result_store.objects.values_list('id','userid')

class SubmitForm(forms.Form):
    user_id = fields.CharField(
        label='用户名',
        widget=widgets.Select())
    inclass_score1 = fields.FloatField(
        max_value=200, min_value=0,
        required=False,
    )
    inclass_score2 = fields.FloatField(
        max_value=200, min_value=0,
        required=False,
    )
    inclass_score3 = fields.FloatField(
        max_value=200, min_value=0,
        required=False,
    )
    inclass_score4 = fields.FloatField(
        max_value=200, min_value=0,
        required=False,
    )
    inclass_score5 = fields.FloatField(
        max_value=200, min_value=0,
        required=False,
    )
    inclass_score6 = fields.FloatField(
        max_value=200, min_value=0,
        required=False,
    )
    view_time = fields.FloatField(
        max_value=1000, min_value=0,
        required=False,
    )
    def __init__(self,*args,**kwargs):
        super(SubmitForm,self).__init__(*args,**kwargs)
        self.fields['user_id'].widget.choices=models.result_store.objects.values_list('userid','userid')



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
        obj = RequestForm(request.POST)
        id = obj.data['user_id']
        ret = models.result_store.objects.filter(id=id)
        user_id = ret[0].userid
        final_score = ret[0].final_score
        return render(request, 'view_score.html',
                          {"obj": obj, 'name': 'test',
                           'student_id': user_id, 'score': final_score})
    return render(request, 'view_score.html', {'name': 'test','obj':RequestForm()})


def add_remove_user(request):
    if request.method == "POST":
        if 'add' in request.POST:
            obj_add = addForm(request.POST)
            user_id = obj_add.data['user_id']
            if models.User.objects.filter(userid=user_id):
                msg = "用户的学号已经存在！"
                return render(request, 'add_remove_user.html',
                              {"obj_add": obj_add, "obj_delete": deleteForm(), 'name': 'admin', 'user_id_add': user_id, 'msg_add': msg})
            else:
                user_name = obj_add.data['user_name']
                user_type = obj_add.data['user_type']
                models.User.objects.create(userid=user_id, username=user_name, password="123456", usertype=user_type)
                if user_type == 'STUDENT':
                    models.result_store.objects.create(userid=user_id, inclass_score1=0, inclass_score2=0, inclass_score3=0,
                                                   inclass_score4=0, inclass_score5=0, inclass_score6=0, final_score=0,
                                                   comment='default')
                msg = "创建成功"
                return render(request, 'add_remove_user.html',
                              {"obj_add": obj_add, "obj_delete": deleteForm(), 'name': 'admin', 'user_id_add': user_id, 'msg_add': msg, 'user_type': user_type})
        if 'delete' in request.POST:
            obj_delete = deleteForm(request.POST)
            user_id = obj_delete.data['user_id']
            if user_id == 'admin':
                return render(request, 'add_remove_user.html',
                              {"obj_add": addForm(), "obj_delete": deleteForm(), 'name': 'admin',
                               'student_id': user_id, 'msg_delete': "不允许删除超级管理员"})
            if not models.User.objects.filter(userid=user_id):
                msg = "待删除用户不存在！"
                return render(request, 'add_remove_user.html',
                              {"obj_add": addForm(), "obj_delete": deleteForm(), 'name': 'admin',
                               'student_id': user_id, 'msg_delete': msg})
            else:
                q1 = models.User.objects.filter(userid=user_id).last()
                q1.delete()
                if models.result_store.objects.filter(userid=user_id):
                    q2 = models.result_store.objects.filter(userid=user_id).last()
                    q2.delete()
                msg = "删除成功"
                return render(request, 'add_remove_user.html',
                              {"obj_add": addForm(), "obj_delete": deleteForm(), 'name': 'admin',
                               'student_id': user_id, 'msg_delete': msg})
    return render(request, 'add_remove_user.html', {"obj_add": addForm(),"obj_delete": deleteForm(), 'name': 'admin'})


def change_permission(request):
    if request.method == "POST":
        obj = deleteForm(request.POST)
        user_id = obj.data['user_id']
        if user_id == 'admin':
            return render(request, 'change_permission.html',
                          {"obj": obj, 'name': 'admin', 'msg': "不允许修改超级管理员权限！"})
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
    obj = deleteForm()
    return render(request, 'change_permission.html', {"obj": obj, 'name': 'admin'})


def self_predict(request):
    if request.method == "POST":
        # 读取模型
            # 之后更新SVM模型后也需要更改路径
        path = r'E:\Study\SSPKU\软件工程\小组课题\git\djangoProject_PES\app01\svm.joblib_231328'
        svm_model = joblib.load(path)

        # 获取数据
        obj = SubmitForm(request.POST)
        data_list = []
        data_list.append(int(obj.data['inclass_score1']))
        data_list.append(int(obj.data['inclass_score2']))
        data_list.append(int(obj.data['inclass_score3']))
        data_list.append(int(obj.data['inclass_score4']))
        data_list.append(int(obj.data['inclass_score5']))
        data_list.append(int(obj.data['inclass_score6']))
        data_list.append(int(obj.data['view_time']))
        # 归一化
        mm = MinMaxScaler()
        data_normal = mm.fit_transform([data_list])
        # 预测
        result_score = svm_model.predict(data_normal)[0]

        return render(request, 'self_predict.html', {"obj": obj, 'name': 'test', 'msg': '你的成绩预测为：', 'result': round(result_score,2)})
    obj = SubmitForm()
    return render(request, 'self_predict.html', {"obj": obj, 'name': 'test'},)

def update_detail(request):
    if request.method == "POST":
        obj = SubmitForm(request.POST)
        user_id = obj.data['user_id']

        ret = models.result_store.objects.get(userid=user_id)
        dict = {}
        dict['inclass_score1'] = obj.data['inclass_score1']
        dict['inclass_score2'] = obj.data['inclass_score2']
        dict['inclass_score3'] = obj.data['inclass_score3']
        dict['inclass_score4'] = obj.data['inclass_score4']
        dict['inclass_score5'] = obj.data['inclass_score5']
        dict['inclass_score6'] = obj.data['inclass_score6']
        dict['view_time'] = obj.data['view_time']
        for i in dict.keys():
            if dict.get(i) != "":
                if i == "inclass_score1":
                    ret.inclass_score1 = dict.get(i)
                if i == "inclass_score2":
                    ret.inclass_score2 = dict.get(i)
                if i == "inclass_score3":
                    ret.inclass_score3 = dict.get(i)
                if i == "inclass_score4":
                    ret.inclass_score4 = dict.get(i)
                if i == "inclass_score5":
                    ret.inclass_score5 = dict.get(i)
                if i == "inclass_score6":
                    ret.inclass_score6 = dict.get(i)
        ret.save()
        msg = "修改成功"

        return render(request, 'update_detail.html',
                      {"obj": obj, 'name': 'admin', 'user_id': user_id, 'msg': msg})
    obj = SubmitForm()
    return render(request, 'update_detail.html', {"obj": obj, 'name': 'admin'})
