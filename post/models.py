from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=128)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()

class Comment(models.Model):
    aid = models.IntegerField()
    name = models.CharField(max_length=128,null=False,blank=False)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()


