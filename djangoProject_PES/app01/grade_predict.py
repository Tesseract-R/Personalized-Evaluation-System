# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 10:27:35 2021

@author: ASUS
"""
import time


import joblib
import pymysql
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score  # 交叉检验
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, r2_score  # 批量导入指标算法
import numpy as np


def grade_predict(host,user_name,key,database_name):
    # 连接数据库
    db = pymysql.connect(host,user_name,key,database_name)
    cursor = db.cursor()
    cursor2 = db.cursor()
    cursor3 = db.cursor()
    
    sql = "SELECT student_id,final_score,Semester_start_score FROM final_score"
    list1 = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            f_id = row[0]
            f_final = row[1]
            f_start = row[2]
            sql2 = "SELECT i.Structured_design, i.Software_process,i.Detailed_design,i.Demand_analysis,i.Tests_for_realization,i.Maintenance,v.viewing_time_length from inclass_test i, viewing_time_ranking v where i.student_id = v.student_id and i.student_id = \"" + f_id + "\""
            
            try:
                cursor2.execute(sql2)
                results2 = cursor2.fetchone()
                fscore0 = results2[0]
                fscore1 = results2[1]
                fscore2 = results2[2]
                fscore3 = results2[3]
                fscore4 = results2[4]
                fscore5 = results2[5]
                viewtime = results2[6]
                list1.append({"student_id": f_id, "Semester_start_score": f_start, "Structured_design": fscore0,
                              "Software_process":fscore1,
                              "Detailed_design":fscore2, "Demand_analysis":fscore3,"Tests_for_realization":fscore4,
                              "Maintenance":fscore5,"final_score":f_final,"viewing_time_length":viewtime})
            except:
                print("Error, unable to fetch data")
    except:
        print("Error, unable to fetch data")
        
    db.close()
    df = pd.DataFrame(list1, columns=['Semester_start_score','Structured_design','Software_process','Detailed_design',
                                      'Demand_analysis','Tests_for_realization','Maintenance','final_score',
                                      'viewing_time_length'])
    # df.to_csv(r"E:\Study\SSPKU\软件工程\小组课题\在线行为数据和期末成绩\score_all.csv", index=False)  # 保存数据


    # 分割训练、测试集 （期末成绩为y值，其他数据为x值）
    print("Splitting training data and testing data...")
    train_x, test_x, train_y, test_y = train_test_split(df[['Semester_start_score', 'Structured_design',
                                                            'Software_process', 'Detailed_design', 'Demand_analysis',
                                                            'Tests_for_realization', 'Maintenance',
                                                            'viewing_time_length']], df['final_score'], test_size=0.1)

    # 特征归一化
    train_y_normal = train_y

    mm = MinMaxScaler()
    train_x_normal = mm.fit_transform(train_x)
    test_x_normal = mm.transform(test_x)

    # 设置超参数
    C = [0.1, 0.2, 0.5, 0.8, 0.9, 1, 2, 5, 10, 100, 1000]
    kernel = 'rbf'
    gamma = [0.001, 0.01, 0.1, 0.2, 0.5, 0.8]
    epsilon = [0.01, 0.05, 0.1, 0.2, 0.5, 0.8, 1, 10, 100]
    # 参数字典
    params_dict = {
        'C': C,
        'gamma': gamma,
        'epsilon': epsilon
    }

    # 初始化支持向量机
    gsCV = GridSearchCV(SVR(kernel='rbf', gamma=100), cv=10, param_grid=params_dict)
    gsCV.fit(train_x_normal, train_y_normal)

    svr = SVR(C=gsCV.best_params_['C'], kernel=kernel, gamma=gsCV.best_params_['gamma'],
              epsilon=gsCV.best_params_['epsilon'])
    svr.fit(train_x_normal, train_y_normal)

    # 用测试集检验误差
    y_svr = svr.predict(test_x_normal)
    mse = mean_squared_error(test_y.values, y_svr)
    return svr, mm, mse, test_y, y_svr

def update_system():
    while(True):
        svr, mm, mse, test_y, y_svr = grade_predict("localhost", "root", "california", "seconddegree")
        print(mse)
        if mse <= 100:
            # 保存模型
            joblib.dump(svr, r'svm.joblib')
            joblib.dump(mm, r'mm')
            return test_y, y_svr, mse
            # return True

if __name__ == '__main__':
    test_y, y_svr, mse = update_system()
    print("预测偏差：", mse)
    
    # 在图上可视化
    X = np.linspace(1,len(y_svr),len(y_svr))
    plt.scatter(X, test_y.values, c='k', label="Final Score", zorder=1)
    plt.scatter(X, y_svr, c='r', label="Predict Score (MSE: %.3f)" % mse)
    plt.xlabel('Student')
    plt.ylabel('Score')
    plt.legend()
    plt.figure()
    plt.show()

