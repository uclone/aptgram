from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Meter(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_meters', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_meters', verbose_name='사용목적')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='사용장소')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='장치종류')
    serial = models.CharField(max_length=100, verbose_name='장치번호')
    monmtr = models.IntegerField(default=0, null=True, blank=True, verbose_name='가스미터사용량')
    moncor = models.IntegerField(default=0, null=True, blank=True, verbose_name='가스보정사용량')
    amtmonmtr = models.IntegerField(default=0, null=True, blank=True, verbose_name='가스미터사용액')
    amtmoncor = models.IntegerField(default=0, null=True, blank=True, verbose_name='가스보정사용액')
    accmtr = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스미터검침')
    acccor = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스보정검침')
    gastmp = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스온도(*C)')
    gasprs = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스압력(kPa)')
    gasalarm = models.CharField(max_length=100, null=True, blank=True, verbose_name='가스알림')
    hometmp = models.IntegerField(default=0, null=True, blank=True,verbose_name='집안온도(*C)')
    homehumid = models.IntegerField(default=0, null=True, blank=True,verbose_name='집안습도(%)')
    homealarm = models.CharField(max_length=100, null=True, blank=True, verbose_name='집안알림')
    valvestatus = models.CharField(max_length=100, null=True, blank=True, verbose_name='가스밸브상태')
    valveaction = models.CharField(max_length=100, null=True, blank=True, verbose_name='가스밸브조작')
    date = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='일시')
    created = models.DateTimeField(auto_now_add=True, verbose_name='일시')
    mk = models.CharField(max_length=100, null=True, blank=True, verbose_name='구글계정과 동일한 패스워드')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M")


    def get_absolute_url(self):
        return reverse('metergram:meter_detail', args=[str(self.id)])


class Smeter(models.Model):
    author = models.CharField(max_length=100, null=True, blank=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, blank=True, verbose_name='사용목적')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='사용장소')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='장치종류')
    serial = models.CharField(max_length=100, verbose_name='장치번호')
    monmtr = models.IntegerField(default=0, null=True, blank=True, verbose_name='가스미터사용량')
    moncor = models.IntegerField(default=0, null=True, blank=True, verbose_name='가스보정사용량')
    amtmonmtr = models.IntegerField(default=0, null=True, blank=True, verbose_name='가스미터사용액')
    amtmoncor = models.IntegerField(default=0, null=True, blank=True, verbose_name='가스보정사용액')
    accmtr = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스미터검침')
    acccor = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스보정검침')
    gastmp = models.IntegerField(default=0, null=True, blank=True, verbose_name='가스온도(*C)')
    gasprs = models.IntegerField(default=0, null=True, blank=True, verbose_name='가스압력(kPa)')
    gasalarm = models.CharField(max_length=100, null=True, blank=True, verbose_name='가스알림')
    hometmp = models.IntegerField(default=0, null=True, blank=True, verbose_name='집안온도(*C)')
    homehumid = models.IntegerField(default=0, null=True, blank=True, verbose_name='집안습도(%)')
    homealarm = models.CharField(max_length=100, null=True, blank=True, verbose_name='집안알림')
    valvestatus = models.CharField(max_length=100, null=True, blank=True, verbose_name='가스밸브상태')
    valveaction = models.CharField(max_length=100, null=True, blank=True, verbose_name='가스밸브조작')
    date = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='일시')
    created = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='일시')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M")

