from django.db import models
from datetime import datetime

# Create your models here.

class Test(models.Model):
    test=models.CharField(max_length=10)
    
    def __str__(self):
        return self.test
    
class Beach(models.Model):
    beach=models.CharField(primary_key=True,max_length=3)
    link_addr=models.TextField(null=True)
    link_tel=models.CharField(null=True,max_length=25)
    lat=models.FloatField(null=True)
    lon=models.FloatField(null=True)
    
class Haeundae(models.Model):
    idx=models.AutoField(primary_key=True)
    wt=models.FloatField(null=True)
    at=models.FloatField(null=True)
    ws=models.FloatField(null=True)
    swh=models.FloatField(null=True)
    score=models.CharField(null=True,max_length=2)
    pred_date=models.DateTimeField(default=datetime.now,blank=True)
    
class Songjung(models.Model):
    idx=models.AutoField(primary_key=True)
    wt=models.FloatField(null=True)
    at=models.FloatField(null=True)
    ws=models.FloatField(null=True)
    swh=models.FloatField(null=True)
    score=models.CharField(null=True,max_length=2)
    pred_date=models.DateTimeField(default=datetime.now,blank=True)
    
class Imrang(models.Model):
    idx=models.AutoField(primary_key=True)
    wt=models.FloatField(null=True)
    at=models.FloatField(null=True)
    ws=models.FloatField(null=True)
    swh=models.FloatField(null=True)
    score=models.CharField(null=True,max_length=2)
    pred_date=models.DateTimeField(default=datetime.now,blank=True)
    
class Score(models.Model):
    idx=models.AutoField(primary_key=True)
    beach=models.CharField(null=True,max_length=3)
    wt=models.FloatField(null=True)
    at=models.FloatField(null=True)
    ws=models.FloatField(null=True)
    swh=models.FloatField(null=True)
    score=models.CharField(null=True,max_length=2)
    date=models.DateTimeField(default=datetime.now,blank=True)
    
class Jellyfish(models.Model):
    idx=models.AutoField(primary_key=True)
    name=models.CharField(null=True,max_length=10)
    ratio=models.FloatField(null=True)
    map=models.TextField(null=True)
    date=models.CharField(null=True,max_length=10)
    
class Weather(models.Model):
    idx=models.AutoField(primary_key=True)
    tos=models.CharField(null=True,max_length=11)
    vof=models.FloatField(null=True)
    wt=models.FloatField(null=True)
    salt=models.FloatField(null=True)
    swh=models.FloatField(null=True)
    ws=models.FloatField(null=True)
    at=models.FloatField(null=True)
    ap=models.FloatField(null=True)
    ratio=models.FloatField(null=True)
    true=models.IntegerField(null=True)
    
class Plankton(models.Model):
    idx=models.AutoField(primary_key=True)
    tos=models.CharField(null=True,max_length=11)
    wt=models.FloatField(null=True)
    yogak=models.FloatField(null=True)
    moak=models.FloatField(null=True)
    dangak=models.FloatField(null=True)
    nbd=models.FloatField(null=True)
    jigak=models.FloatField(null=True)
    chuck=models.FloatField(null=True)
    yagwang=models.FloatField(null=True)
    jf=models.FloatField(null=True)
    LARVAE=models.FloatField(null=True)
    others=models.FloatField(null=True)
    organic=models.FloatField(null=True)
    ratio=models.FloatField(null=True)
    true=models.IntegerField(null=True)