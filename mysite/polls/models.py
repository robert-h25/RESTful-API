from django.db import models

# Create your models here.
class Story(models.Model):
    key = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=64)
    region = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    author = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    details = models.CharField(max_length=128)