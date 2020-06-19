from django.db import models

class Resident(models.Model):
    dong = models.CharField(max_length=10, verbose_name = "동")
    ho = models.CharField(max_length=10, verbose_name = "호")
    represent = models.CharField(max_length=20)
    family = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date = models.DateField()
    car = models.CharField(max_length=100)
    remark = models.CharField(max_length=100)

