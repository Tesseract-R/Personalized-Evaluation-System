from django.shortcuts import render, HttpResponse, redirect
from app01 import models
import pymysql

import pymysql

# Create your views here.


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

    # 连接database
    conn = pymysql.connect("localhost", "root", "california", "seconddegree")

    # 查询期末成绩
    try:
        # 得到一个可以执行SQL语句的光标对象
        cursor1 = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        sql = "SELECT final_score FROM final_score where student_id = '" + name + "'";
        # 执行SQL语句
        cursor1.execute(sql)
        results = cursor1.fetchall()
        cursor1.close()
    except:
        print("查询失败")
    final_score = results[0][0]
    # 查询平时成绩
    try:
        # 得到一个可以执行SQL语句的光标对象
        cursor2 = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        sql = "SELECT * FROM inclass_test where student_id = '" + name + "'";
        # 执行SQL语句
        cursor2.execute(sql)
        results = cursor2.fetchall()
        cursor2.close()
    except:
        print("查询失败")
    structure_design = results[0][1]
    software_process = results[0][2]
    detailed_design = results[0][3]
    demand_analysis = results[0][4]
    realization = results[0][5]
    maintenance = results[0][6]

    return render(request, 'studentindex.html', {'name': name,'structure_design':structure_design,'software_process':software_process,
                                                 'detailed_design':detailed_design,'demand_analysis':demand_analysis,
                                                 'relization':realization,'maintenance':maintenance,'final_score':final_score})

def index(request):

    # 返回结果
    error_msg = ""
    if request.method == "POST":
        user = request.POST['username']
        pwd = request.POST['password']
        if not models.User.objects.filter(username=user):
            error_msg = "登录失败，该用户不存在！"
            return render(request, 'index.html', {"error": error_msg})

        ret = models.User.objects.filter(username=user, password=pwd)
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

    return render(request, 'index.html',{"error":error_msg})

def logout(request):
    return HttpResponse("登出成功！请关闭页面。")


def view_score(request):
    print(request)
    if request.method == "POST":
        user_name = request.POST['001']
        print(user_name)
        if not models.result_store.objects.filter(username=user_name):
            return_value = "该学生不存在！"
        else:
            ret = models.result_store.objects.filter(username=user_name)
            return_value = ret[0].score
        return render(request, 'view_score.html',{'name':'test', 'student_id':user_name, 'score':return_value})
    return render(request, 'view_score.html',{'name':'test'})