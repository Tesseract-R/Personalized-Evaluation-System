from django.db import models


# Create your models here.
class User(models.Model):
    userid = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    usertype = models.CharField(max_length=32) # 用户类型：老师、助教、学生、管理员


class result_store(models.Model):
    userid = models.CharField(max_length=32)
    inclass_score1 = models.FloatField(max_length=32)
    inclass_score2 = models.FloatField(max_length=32)
    inclass_score3 = models.FloatField(max_length=32)
    inclass_score4 = models.FloatField(max_length=32)
    inclass_score5 = models.FloatField(max_length=32)
    inclass_score6 = models.FloatField(max_length=32)
    final_score = models.FloatField(max_length=32)
    comment = models.CharField(max_length=2048)