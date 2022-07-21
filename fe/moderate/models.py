from django.db import models

# Create your models here.
class Module(models.Model):
    code = models.CharField(max_length = 10)
    rating = models.FloatField(default = 0.0)
    comment1 = models.CharField(max_length = 1000, default = "")
    comment2 = models.CharField(max_length = 1000, default = "")
    comment3 = models.CharField(max_length = 1000, default = "")
    searched = models.IntegerField(default = 1)
    emotions = models.CharField(max_length = 1000, default = "1.0,1.0,1.0,1.0,1.0")
    #slug = models.SlugField(max_length=350)

class Issue(models.Model):
    code = models.CharField(max_length = 10, default = "")
    message = models.CharField(max_length=500, default = "")
    #slug = models.SlugField(max_length=350)