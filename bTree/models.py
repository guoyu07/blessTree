from django.db import models

# Create your models here.
class User(models.Model):
    appid = models.CharField(max_length=200);
