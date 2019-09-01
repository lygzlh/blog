from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)


class Article(models.Model):
    title = models.CharField(max_length=32)
    introduce = models.CharField(max_length=255)
    content = models.TextField()
    date = models.FloatField()
    author = models.ForeignKey(to='UserInfo',to_field='id',on_delete=models.CASCADE)
    category = models.ForeignKey(to='Category', to_field='id', on_delete=models.CASCADE)

class Category(models.Model):
    classify = models.CharField(max_length=32)
