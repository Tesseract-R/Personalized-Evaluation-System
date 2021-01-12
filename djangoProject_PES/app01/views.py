import os
import joblib
from django.core.exceptions import ValidationError
from django.http import FileResponse
from django.shortcuts import render, HttpResponse, redirect
from app01 import models, grade_predict
from django import forms
from django.forms import fields
from django.forms import widgets

from sklearn.preprocessing import MinMaxScaler


# Create your views here.

class addForm(forms.Form):
    # 增加用户表单
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
    # 删除用户表单
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

    def __init__(self, *args, **kwargs):
        super(deleteForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].widget.choices = models.User.objects.values_list('userid', 'username')


class RequestForm(forms.Form):
    # 用于查询学生信息的表单
    user_id = fields.CharField(
        label='学生学号',
        widget=widgets.Select())

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].widget.choices = models.result_store.objects.values_list('id', 'userid')


class SubmitForm(forms.Form):
    # 修改学生信息的表单
    user_id = fields.CharField(
        label='用户名',
        widget=widgets.Select())
    start_score = fields.FloatField(
        max_value=200, min_value=0,
        required=False,
    )
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

    def __init__(self, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].widget.choices = models.result_store.objects.values_list('userid', 'userid')


class PredictForm(forms.Form):
    # 自助预测成绩的表单
    start_score = fields.FloatField(
        max_value=200, min_value=0,
    )
    inclass_score1 = fields.FloatField(
        max_value=200, min_value=0,
    )
    inclass_score2 = fields.FloatField(
        max_value=200, min_value=0,
    )
    inclass_score3 = fields.FloatField(
        max_value=200, min_value=0,
    )
    inclass_score4 = fields.FloatField(
        max_value=200, min_value=0,
    )
    inclass_score5 = fields.FloatField(
        max_value=200, min_value=0,
    )
    inclass_score6 = fields.FloatField(
        max_value=200, min_value=0,
    )
    view_time = fields.FloatField(
        max_value=1000, min_value=0,
    )


class passwordForm(forms.Form):
    # 修改密码的表单
    original_password = fields.CharField(
        required=True,
        widget=forms.PasswordInput,
    )
    new_password = fields.CharField(
        required=True,
        widget=forms.PasswordInput,
    )
    confirm_password = fields.CharField(
        required=True,
        widget=forms.PasswordInput,
    )


def adminindex(request):
    """
    导向管理员主页
    :param request:
    :return:
    """
    name = request.session.get('user_name')
    return render(request, 'adminindex.html', {'name': name})


def teacherindex(request):
    """
    导向教师主页
    :param request:
    :return:
    """
    name = request.session.get('user_name')
    return render(request, 'teacherindex.html', {'name': name})


def studentindex(request):
    """
    导向学生主页
    :param request:
    :return:
    """
    userid = request.session.get('user_id')
    name = request.session.get('user_name')

    ret = models.result_store.objects.filter(userid=userid)
    start_score = ret[0].start_score
    structure_design = ret[0].inclass_score1
    software_process = ret[0].inclass_score2
    detailed_design = ret[0].inclass_score3
    demand_analysis = ret[0].inclass_score4
    realization = ret[0].inclass_score5
    maintenance = ret[0].inclass_score6
    final_score = ret[0].final_score
    comment = ret[0].comment
    if len(comment) > 100:
        comment = comment[:100] + "......"
    return render(request, 'studentindex.html',
                  {'name': name, 'start_score':start_score,'structure_design': structure_design, 'software_process': software_process,
                   'detailed_design': detailed_design, 'demand_analysis': demand_analysis,
                   'realization': realization, 'maintenance': maintenance, 'final_score': final_score,
                   'comment': comment})


def index(request):
    """
    登录界面，在user的表中查询是否有匹配的用户名和密码，验证通过后根据角色不同导向
    adminindex、studentindex和teacherindex三个页面
    :param request:
    :return:
    """
    error_msg = ""
    if request.method == "POST":
        user = request.POST['username']
        pwd = request.POST['password']
        if not models.User.objects.filter(userid=user):
            error_msg = "登录失败，该用户不存在！"
            return render(request, 'index.html', {"error": error_msg})

        ret = models.User.objects.filter(userid=user, password=pwd)
        if ret:  # 登陆成功
            request.session['is_login'] = True
            request.session['user_id'] = ret[0].userid
            request.session['user_name'] = ret[0].username
            request.session['user_type'] = ret[0].usertype
            if ret[0].usertype == 'ADMIN':  # 根据用户身份导向不同的页面
                return adminindex(request)
            elif ret[0].usertype == 'TEACHER' or ret[0].usertype == 'TA':
                return teacherindex(request)
            elif ret[0].usertype == 'STUDENT':
                return studentindex(request)
            else:
                return studentindex(request)
        else:
            error_msg = "登录失败，请检查用户名和密码！"

    return render(request, 'index.html', {"error": error_msg})


def logout(request):
    """
    登出
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return HttpResponse("登出成功！请关闭页面。")


def view_score(request):
    """
    在数据库中查询学生预测的成绩
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect("/index/")
    name = request.session.get('user_name')
    html = 'view_score.html'
    if request.session.get('user_type') == 'ADMIN':
        html = 'admin_' + html

    if request.method == "POST":
        obj = RequestForm(request.POST)
        id = obj.data['user_id']
        ret = models.result_store.objects.filter(id=id)
        user_id = ret[0].userid
        final_score = ret[0].final_score
        return render(request, html,
                      {"obj": obj, 'name': name,
                       'student_id': user_id, 'score': final_score})
    return render(request, html, {'name': name, 'obj': RequestForm()})


def view_detail(request):
    """
    在数据库中查询学生平时成绩
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect("/index/")
    name = request.session.get('user_name')
    html = 'view_detail.html'
    if request.session.get('user_type') == 'ADMIN':
        html = 'admin_' + html

    if request.method == "POST":
        obj = RequestForm(request.POST)
        id = obj.data['user_id']
        ret = models.result_store.objects.filter(id=id)
        user_id = ret[0].userid
        start_score = ret[0].start_score
        inclass_score1 = ret[0].inclass_score1
        inclass_score2 = ret[0].inclass_score2
        inclass_score3 = ret[0].inclass_score3
        inclass_score4 = ret[0].inclass_score4
        inclass_score5 = ret[0].inclass_score5
        inclass_score6 = ret[0].inclass_score6
        view_time = ret[0].view_time
        return render(request, html,
                      {"obj": obj, 'name': name,
                       'student_id': user_id, 'start_score':start_score, 'inclass_score1': inclass_score1, 'inclass_score2': inclass_score2,
                       'inclass_score3': inclass_score3, 'inclass_score4': inclass_score4,
                       'inclass_score5': inclass_score5, 'inclass_score6': inclass_score6, 'view_time':view_time})
    return render(request, html, {'name': name, 'obj': RequestForm()})


def view_evaluation(request):
    """
    在数据库中查询学生的个性化评价
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect("/index/")
    name = request.session.get('user_name')
    html = 'view_evaluation.html'
    if request.session.get('user_type') == 'ADMIN':
        html = 'admin_' + html
    if request.method == "POST":
        obj = RequestForm(request.POST)
        id = obj.data['user_id']
        ret = models.result_store.objects.filter(id=id)
        user_id = ret[0].userid
        comment = ret[0].comment
        generatePDF(comment)
        return render(request, html,
                      {"obj": obj, 'name': name,
                       'student_id': user_id, 'comment': comment, 'button': '下载'})
    return render(request, html, {'name': name, 'obj': RequestForm()})


def generatePDF(comment):
    """
    根据内容生成一个PDF文件
    :param comment:
    :return:
    """
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    from reportlab.platypus import SimpleDocTemplate, Paragraph

    str1 = comment
    pdfmetrics.registerFont(TTFont('fs', 'simfang.ttf'))  # 注册字体
    mystyle = ParagraphStyle(name="user_style", fontName="fs", alignment=TA_LEFT, )
    pdf = SimpleDocTemplate('comment.pdf')
    contents = []
    for i in str1.split('\n'):
        contents.append(Paragraph(i, style=mystyle))
    pdf.build(contents)


def download(request):
    """
    下载（目前没办法应对并发的下载请求）
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect("/index/")
    name = request.session.get('user_name')
    if os.path.exists('comment.pdf'):
        file = open('comment.pdf', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="comment.pdf"'
        return response
    return render(request, 'view_evaluation.html', {'name': name, 'obj': RequestForm()})


def add_remove_user(request):
    """
    增加或删除用户，根据POST中按钮的名称判断提交的请求
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect("/index/")
    name = request.session.get('user_name')
    if request.method == "POST":
        if 'add' in request.POST:
            obj_add = addForm(request.POST)
            user_id = obj_add.data['user_id']
            if models.User.objects.filter(userid=user_id):
                msg = "用户的学号已经存在！"
                return render(request, 'add_remove_user.html',
                              {"obj_add": obj_add, "obj_delete": deleteForm(), 'name': name, 'user_id_add': user_id,
                               'msg_add': msg})
            else:
                user_name = obj_add.data['user_name']
                user_type = obj_add.data['user_type']
                models.User.objects.create(userid=user_id, username=user_name, password="123456", usertype=user_type)
                if user_type == 'STUDENT':
                    models.result_store.objects.create(userid=user_id, start_score=0,inclass_score1=0, inclass_score2=0,
                                                       inclass_score3=0,
                                                       inclass_score4=0, inclass_score5=0, inclass_score6=0,
                                                       final_score=0,view_time=0,
                                                       comment='default')
                msg = "创建成功"
                return render(request, 'add_remove_user.html',
                              {"obj_add": obj_add, "obj_delete": deleteForm(), 'name': name, 'user_id_add': user_id,
                               'msg_add': msg, 'user_type': user_type})
        if 'delete' in request.POST:
            obj_delete = deleteForm(request.POST)
            user_id = obj_delete.data['user_id']
            if user_id == 'admin':
                return render(request, 'add_remove_user.html',
                              {"obj_add": addForm(), "obj_delete": deleteForm(), 'name': name,
                               'student_id': user_id, 'msg_delete': "不允许删除超级管理员"})
            if not models.User.objects.filter(userid=user_id):
                msg = "待删除用户不存在！"
                return render(request, 'add_remove_user.html',
                              {"obj_add": addForm(), "obj_delete": deleteForm(), 'name': name,
                               'student_id': user_id, 'msg_delete': msg})
            else:
                q1 = models.User.objects.filter(userid=user_id).last()
                q1.delete()
                if models.result_store.objects.filter(userid=user_id):
                    q2 = models.result_store.objects.filter(userid=user_id).last()
                    q2.delete()
                msg = "删除成功"
                return render(request, 'add_remove_user.html',
                              {"obj_add": addForm(), "obj_delete": deleteForm(), 'name': name,
                               'student_id': user_id, 'msg_delete': msg})
    return render(request, 'add_remove_user.html', {"obj_add": addForm(), "obj_delete": deleteForm(), 'name': name})


def update_permission(request):
    """
    修改用户的权限
    （漏洞：最好验证访问该页面的是管理员）
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect("/index/")
    name = request.session.get('user_name')
    if request.method == "POST":
        obj = deleteForm(request.POST)
        user_id = obj.data['user_id']
        if user_id == 'admin':
            return render(request, 'update_permission.html',
                          {"obj": obj, 'name': name, 'msg': "不允许修改超级管理员权限！"})
        if not models.User.objects.filter(userid=user_id):
            msg = "用户不存在！"
            return render(request, 'update_permission.html',
                          {"obj": obj, 'name': name, 'user_id': user_id, 'msg': msg})
        else:
            ret = models.User.objects.filter(userid=user_id)
            type_before = ret[0].usertype
            ret = models.User.objects.get(userid=user_id)
            type_after = obj.data['user_type']
            ret.usertype = type_after
            ret.save()
            msg = "修改权限成功"
            return render(request, 'update_permission.html',
                          {"obj": obj, 'name': name, 'user_id': user_id, 'msg': msg,
                           'type_before': type_before, 'type_after': type_after})
    obj = deleteForm()
    return render(request, 'update_permission.html', {"obj": obj, 'name': name})


def self_predict(request):
    """
    学生填写成绩表单，然后调用svm模型得到预测的成绩
    :param request:
    :return:
    """
    if request.method == "POST":
        # 读取模型
        # 之后更新SVM模型后也需要更改路径
        path = r'E:\Study\SSPKU\软件工程\小组课题\git\djangoProject_PES\app01\svm.joblib'
        svm_model = joblib.load(path)

        # 获取数据
        obj = PredictForm(request.POST)
        data_list = []
        data_list.append(int(obj.data['start_score']))
        data_list.append(int(obj.data['inclass_score1']))
        data_list.append(int(obj.data['inclass_score2']))
        data_list.append(int(obj.data['inclass_score3']))
        data_list.append(int(obj.data['inclass_score4']))
        data_list.append(int(obj.data['inclass_score5']))
        data_list.append(int(obj.data['inclass_score6']))
        data_list.append(int(obj.data['view_time']))
        # 归一化
        path = r'E:\Study\SSPKU\软件工程\小组课题\git\djangoProject_PES\app01\mm'
        mm = joblib.load(path)
        data_normal = mm.transform([data_list])
        # 预测
        result_score = svm_model.predict(data_normal)[0]

        return render(request, 'self_predict.html',
                      {"obj": obj, 'name': 'test', 'msg': '你的成绩预测为：', 'result': round(result_score, 2)})
    obj = PredictForm()
    return render(request, 'self_predict.html', {"obj": obj, 'name': 'test'}, )


def update_detail(request):
    """
    修改学生信息
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect("/index/")
    name = request.session.get('user_name')
    html = 'update_detail.html'
    if request.session.get('user_type') == 'ADMIN':
        html = 'admin_' + html

    if request.method == "POST":
        obj = SubmitForm(request.POST)
        user_id = obj.data['user_id']

        ret = models.result_store.objects.get(userid=user_id)
        dict = {}
        dict['start_score'] = obj.data['start_score']
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
                    ret.start_score = dict.get(i)
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
                if i == "view_time":
                    ret.view_time = dict.get(i)
        ret.save()
        msg = "修改成功"
        return render(request, html,
                      {"obj": obj, 'name': 'admin', 'user_id': user_id, 'msg': msg})
    obj = SubmitForm()
    return render(request, html, {"obj": obj, 'name': name})


def update_system(request):
    """
    版本更新
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect("/index/")
    # 获取最新version_id
    name = request.session.get('user_name')
    import os
    import time
    path = r'E:\Study\SSPKU\软件工程\小组课题\git\djangoProject_PES\app01\svm.joblib'
    mtime = os.stat(path).st_mtime
    file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))

    if request.method == "POST":
        # 调用svm提供的接口，生成新的模型
        if 'model' in request.POST:
            if grade_predict.update_system():
                msg = "系统更新成功"
                path = r'E:\Study\SSPKU\软件工程\小组课题\git\djangoProject_PES\app01\svm.joblib'
                mtime = os.stat(path).st_mtime
                file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                return render(request, 'update_system.html', {'version_id': file_modify_time, 'msg': msg, 'name': 'admin'})
        # 使用模型更新学生成绩
        elif 'predict_score' in request.POST:
            # 读取模型
            # 之后更新SVM模型后也需要更改路径
            svm_model = joblib.load(r'E:\Study\SSPKU\软件工程\小组课题\git\djangoProject_PES\app01\svm.joblib')
            mm = joblib.load(r'E:\Study\SSPKU\软件工程\小组课题\git\djangoProject_PES\app01\mm')

            ret = models.result_store.objects.filter()
            data_all = []
            for i in ret:
                data_list = []
                data_list.append(i.start_score)
                data_list.append(i.inclass_score1)
                data_list.append(i.inclass_score2)
                data_list.append(i.inclass_score3)
                data_list.append(i.inclass_score4)
                data_list.append(i.inclass_score5)
                data_list.append(i.inclass_score6)
                data_list.append(i.view_time)
                # 归一化
                data_all.append(data_list)
            # 预测
            data_normal = mm.transform(data_all)
            result_score = svm_model.predict(data_normal)
            for i in range(len(ret)):
                object = models.result_store.objects.get(userid=ret[i].userid)
                object.final_score = result_score[i]
                object.save()
            update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            msg = update_time + "更新成功"
            return render(request, 'update_system.html', {'version_id': file_modify_time, 'msg': msg, 'name': 'admin'})
        # 调用评价模块的接口，更新学生的评价
        elif 'evaluation' in request.POST:
            from app01 import stat
            ret = models.result_store.objects.filter()
            for i in range(len(ret)):
                object = models.result_store.objects.get(userid=ret[i].userid)
                object.comment = stat.generate_comment(ret[i].userid)
                object.save()
            update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            msg = update_time + "更新成功"
            return render(request, 'update_system.html', {'version_id': file_modify_time, 'msg': msg, 'name': 'admin'})
    return render(request, 'update_system.html', {'version_id': file_modify_time, 'name': name})


def comment_detail(request):
    """
    学生查看评价的详细内容
    :param request:
    :return:
    """
    userid = request.session.get('user_id')
    ret = models.result_store.objects.filter(userid=userid)
    structure_design = ret[0].inclass_score1
    software_process = ret[0].inclass_score2
    detailed_design = ret[0].inclass_score3
    demand_analysis = ret[0].inclass_score4
    realization = ret[0].inclass_score5
    maintenance = ret[0].inclass_score6
    final_score = ret[0].final_score
    comment = ret[0].comment
    return FileResponse(comment)


### 修改密码模块 ###
def update_password(request):
    """
    修改密码
    需要输入原密码，输入两遍新密码
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect("/index/")
    # 获取最新version_id
    userid = request.session.get('user_id')
    name = request.session.get('user_name')
    if request.method == "POST":
        # 检查原密码是否正确
        obj = passwordForm(request.POST)
        ret = models.User.objects.filter(userid=userid)
        pwd = ret[0].password
        if obj.data['original_password'] != pwd:
            msg = '原密码输入错误'
            return render(request, 'update_password.html', {"obj": obj, 'name': name, 'msg': msg})
        # 检查两遍密码是否一致
        if obj.data['new_password'] != obj.data['confirm_password']:
            msg = '两次密码不一致'
            return render(request, 'update_password.html', {"obj": obj, 'name': name, 'msg': msg})
        # 修改
        ret = models.User.objects.get(userid=userid)
        ret.password = obj.data['new_password']
        ret.save()
        msg = '修改成功'
        return render(request, 'update_password.html', {"obj": passwordForm(), 'name': name, 'msg': msg})
    obj = passwordForm()
    return render(request, 'update_password.html', {"obj": obj, 'name': name})

def visualize(request):#views.py给js传值要注意｜safe以及json5.dumps()
    from app01 import stat
    student_id=request.session.get("user_id")
    a=stat.generate_comment(student_id)
    return render(request,'visualize.html',{'val1':a})