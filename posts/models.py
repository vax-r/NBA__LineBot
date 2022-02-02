
# Create your models here.
from django.db import models
from django.utils import timezone
# 景點位置
class Location(models.Model):
    name = models.CharField(max_length=255)  #位置名稱
#景點貼文
class Post(models.Model):
    subject = models.CharField(max_length=255)  #標題
    content = models.CharField(max_length=255)  #內容
    author = models.CharField(max_length=20)  #貼文者
    create_date = models.DateField(default=timezone.now)  #貼文時間
    location = models.ForeignKey(Location, on_delete=models.CASCADE) 
