from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    usertype = models.CharField(max_length=32) # 用户类型：老师、助教、学生、管理员


class result_store(models.Model):
    username = models.CharField(max_length=32)
    score = models.FloatField(max_length=32)
    comment = models.CharField(max_length=2048)