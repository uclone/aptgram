from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Meter(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_meters', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_meters', verbose_name='아파트명')
    dong = models.CharField(max_length=100, null=True, blank=True, verbose_name='동')
    ho = models.CharField(max_length=100, null=True, blank=True, verbose_name='호')
    mtr = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스미터검침')
    cor = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스보정검침')
    elec = models.IntegerField(default=0, null=True, blank=True,verbose_name='전기검침')
    water = models.IntegerField(default=0, null=True, blank=True,verbose_name='수도검침')
    created = models.DateTimeField(auto_now_add=True, verbose_name='검침일자')
    action = models.CharField(max_length=100, default="검침", verbose_name='처리현황')
    charge = models.CharField(max_length=100, null=True, blank=True, verbose_name='검침담당')
    manager = models.CharField(max_length=100, null=True, blank=True, verbose_name='관리담당')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")


    def get_absolute_url(self):
        return reverse('metergram:meter_detail', args=[str(self.id)])


class Smeter(models.Model):
    author = models.CharField(max_length=100, default="원격검침", verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='아파트명')
    dong = models.CharField(max_length=100, null=True, verbose_name='동')
    ho = models.CharField(max_length=100, null=True, verbose_name='호')
    mtr = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스미터검침')
    cor = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스보정검침')
    elec = models.IntegerField(default=0, null=True, blank=True,verbose_name='전기점검')
    water = models.IntegerField(default=0, null=True, blank=True,verbose_name='수도점검')
    created = models.DateTimeField(blank=True, default=timezone.now, verbose_name='검침일자')
    action = models.CharField(max_length=100, default="검침", verbose_name='처리현황')
    charge = models.CharField(max_length=100, null=True, verbose_name='검침담당')
    manager = models.CharField(max_length=100, null=True, verbose_name='관리담당')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

