import random
import json5
from django.db import connection
import pandas as pd


def activity_count(student_id):
    cursor=connection.cursor()
    cursor.execute("select count(Activity_code) from \
    student_activity_records where student_id=\'"+student_id+'\'')
    data=cursor.fetchall()
    if len(data)>0:
        data=data[0][0]
        return data
    else:
        return 0

def activity_freq(student_id,code):#行为频率
    cursor=connection.cursor()
    cursor.execute("select count(Activity_code) from \
    student_activity_records where student_id=\'"+student_id+'\'\
    and Activity_code=\''+str(code)+'\'')
    data=cursor.fetchall()
    if len(data)>0:
        data=data[0][0]
        all=activity_count(student_id)
        print(all)
        if all>0:
            freq=round(data/all,3)
        else:
            freq=-1
        return freq
    else:
        return -1

def viewing_time(student_id):#观看时长得分
    cursor=connection.cursor()
    cursor.execute("select `rank` from \
    viewing_time_ranking where student_id=\'"+student_id+'\'')
    data=cursor.fetchall()#rank是保留字
    if len(data)>0:
        data=data[0][0]
    else:
        return -1
    cursor.execute("select max(`rank`) from \
    viewing_time_ranking")
    all=cursor.fetchall()
    if len(all)>0:
        all=all[0][0]
        score=(all-data+1)/all*100
        return score
    else:
        return -1

def score_list(student_id):#课堂测验表现
    cursor=connection.cursor()
    cursor.execute("select * from \
    inclass_test where student_id=\'"+student_id+'\'')
    data=cursor.fetchall()
    if len(data)>0:
        data=data[0]
        l=[]
        try:
            for i in range(1,len(data)):
                if data[i]!='':#注意三点：1.表格的数据类型（特殊的object数值型)
                #2.某些行为表里的学号未出现，3.表内有空字符串
                    l.append(data[i])
                else:
                    l.append(-1)
            return l
        except:
            return -1
    else:
        return -1

def scoreAVG(student_id):#课堂测验表现
    cursor=connection.cursor()
    cursor.execute("select * from \
    inclass_test where student_id=\'"+student_id+'\'')
    data=cursor.fetchall()
    if len(data)>0:
        data=data[0]
        sum=0
        try:
            for i in range(1,len(data)):
                if data[i]!='':#注意三点：1.表格的数据类型（特殊的object数值型)
                #2.某些行为表里的学号未出现，3.表内有空字符串
                    sum+=data[i]
            avg=sum/(len(data)-1)
            return avg
        except:
            return -1
    else:
        return -1


# 生成对章节测试的评价
def test_comment(student_id):
    stu=score_list(student_id)
    if stu==-1:
        return '无课堂测验记录'

    chapters = ["结构化设计","软件过程","详细设计","需求分析",
                '实现-测试','系统维护']
    thresholds_neg = [25,25,95,20,23,65]
    thresholds_pos = [35,35,100,32,35,85]
    
    # 记录章节列表
    pos_list, neg_list, other_list = [], [], []
    
    # 遍历
    for i in range(len(chapters)):
        if stu[i] >= thresholds_pos[i]:
            pos_list.append(chapters[i])
        elif stu[i] <= thresholds_neg[i] and stu[i]>=0:
            neg_list.append(chapters[i])
        elif stu[i] > thresholds_neg[i] and stu[i] < thresholds_pos[i]:
            other_list.append(chapters[i])
        else:
            0
    pos_str, other_str ,neg_str = "", "", ""
    if pos_list:
        pos_chapter = "、".join(pos_list)
        pos_str = random.choice(["你对"+ pos_chapter + "等章节的掌握比较熟练，能够熟练地运用所学知识。", 
                                 "你在学习" + pos_chapter + "章节时对内容的理解比较深刻，能够把所学的知识运用起来。",
                                 "你比较喜欢" + pos_chapter + "等章节的内容，能够理解所学知识。*⸜( •ᴗ• )⸝*"
                                ])
    if other_list:
        other_chapter = "、".join(other_list)
        other_str = random.choice(["对于"+ other_chapter + "，你的掌握程度还可以，能够理解老师上课讲的内容，但在运用方面还有进步空间。",
                                   "针对"+ other_chapter + "等章节，你能够基本掌握所学内容，但距离完全理解还有一点距离。(ノ・_・)ノ",
                                   "学习"+ other_chapter + "章节时，大部分知识可以掌握，继续加油!争取完全理解所学知识"
                                ])
    if neg_list:
        neg_chapter = "、".join(neg_list)
        neg_str = random.choice(["你对"+ neg_chapter + "等章节的掌握存在不足，不能够熟练地运用所学知识。", 
                                 "你在学习" + neg_chapter + "章节时对内容的理解还不够深刻，在知识运用方面有待进步。",
                                 "你比较不善于" + neg_chapter + "等章节的内容，还存在很多需要进步的地方。"
                                ])
    

    
    return pos_str + other_str + neg_str

# 生成对moodle平台的评价
def moodle_comment(student_id):
    viewing_time_score=viewing_time(student_id)
    if viewing_time_score==-1:
        return "无moodle视频观看记录"

    if viewing_time_score > 66.7:
        return random.choice(["你从开学到现在在moodle平台上的学习时间较长，请继续保持。:-)",
                             "moodle平台是课余学习的好帮手，到目前为止，你在moodle平台上的学习时间名列前茅，请保持当前的观看习惯。",
                             "从开学到现在，你在moodle平台上的学习时间充足，请保持好当前观看状态。"])
    elif viewing_time_score <33.3:
        return random.choice(["你从开学到现在在moodle平台上的学习时间比较少，在线视频能够帮助你补充在课堂上没有听懂或者遗漏的知识点。",
                             "moodle平台是课余学习的好帮手，到目前为止，你在moodle平台上的学习时间不达标，通过在线视频，你可以复习课堂上讲的难点还可以补充课堂上没有提到的知识点。",
                             "从开学到现在，你在moodle平台上的学习时间排名较为靠后，多通过moodle平台学习有助于你掌握本门课的知识。_(:τ」∠)_"])
    else:
        return random.choice(["你从开学到现在在moodle平台上的学习时间达标，可以在保持原来习惯的基础上可以适当增加自己的观看时间。",
                             "moodle平台是课余学习的好帮手，到目前为止，你在moodle平台上的学习时间合格，可以多通过在线视频的方式巩固自己薄弱的知识点。",
                             "从开学到现在，你在moodle平台上的学习时间达到中等水平，通过在线学习，可以补充课堂上没有提到的知识点，同时有助于对难点的掌握。"])

# 生成moodle学习表现的评价
def moodle_performance_comment(student_id):
    activity_freq_stu=activity_freq(student_id,11)
    count_num = random.choice(["到目前为止","截至目前"])
    
    if activity_freq_stu<=0.05 and activity_freq_stu>=0:
        return count_num + random.choice(["你的moodle学习表现很积极，这是一个很棒的状态，请继续保持！",
                                         "你的moodle学习状态很棒，请保持好当前状态！",
                                         "你的moodle学习参与度很好，希望你继续加油！"]) 
    elif activity_freq_stu>=0.3:
        return count_num + random.choice(["你的moodle学习表现有待提高，还需要更加努力提升自己在moodle上的学习，才能够更好的把握本门课的学习重点。",
                                         "你的moodle学习表现不够积极，要注意提升在moodle上的学习，才能获得高效的学习过程。",
                                         "你的moodle学习表现还有较大提升空间，你需要更加努力提升自己在moodle课堂上的学习，才能获得高效的学习过程。"])
    elif activity_freq_stu<0:
        return count_num+'系统中没有你的moodle学习记录'
    else:
        return count_num + random.choice(["你的moodle学习表现良好，希望你能够继续坚持下去，同时增加自己在moodle上学习的情况。",
                                          "你的moodle学习表现良好，可以尝试在moodle上多多学习，提高自己的知识水平。",
                                          "你的moodle学习表现良好，可以尝试在moodle上多多学习，参与到本门课程的各种教学活动中来。"
            
        ]) 


# 生成对平时测验平均成绩的评价
def average_score_comment(student_id):
    score=scoreAVG(student_id)
    if score==-1:
        return ''

    corpus = random.choice(["按照目前你的平时测验平均成绩，",
                           "根据你的平时测验平均成绩,",
                           "通过统计你的平时测验平均成绩,"])

    if score >52 :
        review = random.choice(["你的成绩是比较不错的，请保持当前的学习状态，继续努力，预祝你期末取得一个好成绩!",
                              "你的成绩很棒，请继续加油，保持好学习状态，预祝你期末取得一个好成绩!"])
    elif score< 42:
        review = random.choice(["你的成绩有待进步，需要在后期付出更多的努力才能得到一个好成绩。",
                              "你的成绩排名较为靠后，请努力加油，调整好学习状态，争取后来居上。"])   
    else:
        review = random.choice(["你的成绩排名中等,继续努力还有进步的空间，祝你期末取得一个好成绩！",
                               "成绩还有进步的空间，需要继续努力,争取取得更高的成绩，相信你可以！"])
    return corpus + review

corpus = "    亲爱的同学们，短短的一个学期即将结束，我们的《软件工程》课程也接近尾声，非常感谢同学们对课程的参与和支持。在期末考试之前，我们根据每位同学的学习状态，生成了一份学习报告，希望对同学们有所帮助:"
happy_new_year1 = "最后，感谢同学们一个学期的不离不弃，高度配合，请同学们多提宝贵意见，我们一定认真学习，持续改进！"

def generate_comment(student_id):
    if score_list(student_id)==-1 and activity_count(student_id)==0 and viewing_time(student_id)==-1:
        return '此用户不存在'
    else:
        res = [corpus,test_comment(student_id),
            moodle_comment(student_id), 
            moodle_performance_comment(student_id), 
            average_score_comment(student_id),
            happy_new_year1]
    #    random.shuffle(res)
        return "\n    ".join(res)