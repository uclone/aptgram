from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse

class Meter(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_meters', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_meters', verbose_name='아파트명')
    dong = models.CharField(max_length=50, null=True, verbose_name='동')
    ho = models.CharField(max_length=50, null=True, verbose_name='호')
    utility = models.CharField(max_length=50, default="수도", verbose_name='종류')
    serial = models.CharField(max_length=20, null=True, verbose_name='기기번호')
    mtr = models.IntegerField(default=0, verbose_name='미터사용량')
    cor = models.IntegerField(default=0, verbose_name='보정사용량')
    amount = models.IntegerField(default=0, verbose_name='요금')
    created = models.DateTimeField(auto_now_add=True, verbose_name='검침일자')
    action = models.CharField(max_length=50, default="검침", verbose_name='처리현황')
    charge = models.CharField(max_length=20, null=True, verbose_name='검침담당')
    manager = models.CharField(max_length=20, null=True, verbose_name='관리담당')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.file.name

    def get_absolute_url_file(self):
        return reverse('metergram:meter_detail', arg=[str(self.id)])


class Smeter(models.Model):
    author = models.CharField(max_length=50, default="원격검침", verbose_name='작성자')
    group = models.CharField(max_length=50, null=True, verbose_name='아파트명')
    dong = models.CharField(max_length=50, null=True, verbose_name='동')
    ho = models.CharField(max_length=50, null=True, verbose_name='호')
    utility = models.CharField(max_length=50, default="수도", verbose_name='종류')
    serial = models.CharField(max_length=20, null=True, verbose_name='기기번호')
    mtr = models.IntegerField(default=0, verbose_name='미터사용량')
    cor = models.IntegerField(default=0, verbose_name='보정사용량')
    amount = models.IntegerField(default=0, verbose_name='요금')
    created = models.DateTimeField(auto_now_add=True, verbose_name='검침일자')
    action = models.CharField(max_length=50, default="검침", verbose_name='처리현황')
    charge = models.CharField(max_length=20, null=True, verbose_name='검침담당')
    manager = models.CharField(max_length=20, null=True, verbose_name='관리담당')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.file.name