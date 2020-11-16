from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Meter(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_meters', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_meters', verbose_name='단지명/시군구')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='세부주소')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='장치종류')
    serial = models.CharField(max_length=100, verbose_name='장치번호')
    mtr = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스미터검침')
    cor = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스보정검침')
    elec = models.IntegerField(default=0, null=True, blank=True,verbose_name='전기검침')
    water = models.IntegerField(default=0, null=True, blank=True,verbose_name='수도검침')
    temp = models.IntegerField(default=0, null=True, blank=True,verbose_name='온도(*C')
    humidity = models.IntegerField(default=0, null=True, blank=True,verbose_name='습도(%)')
    usegas = models.CharField(max_length=100, null=True, blank=True, verbose_name='가스상태')
    usewater = models.CharField(max_length=100, null=True, blank=True, verbose_name='수도상태')
    alarm = models.CharField(max_length=100, null=True, blank=True, verbose_name='경보내용')
    actgas = models.CharField(max_length=100, null=True, blank=True, verbose_name='가스조치요청')
    actalarm = models.CharField(max_length=100, null=True, blank=True, verbose_name='경보조치요청')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name='참고사항')
    date = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='일시')
    created = models.DateTimeField(auto_now_add=True, verbose_name='일시')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")


    def get_absolute_url(self):
        return reverse('metergram:meter_detail', args=[str(self.id)])


class Smeter(models.Model):
    author = models.CharField(max_length=100, null=True, blank=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, blank=True, verbose_name='단지명/시군구')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='세부주소')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='장치종류')
    serial = models.CharField(max_length=100, verbose_name='장치번호')
    mtr = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스미터검침')
    cor = models.IntegerField(default=0, null=True, blank=True,verbose_name='가스보정검침')
    elec = models.IntegerField(default=0, null=True, blank=True,verbose_name='전기점검')
    water = models.IntegerField(default=0, null=True, blank=True,verbose_name='수도점검')
    temp = models.IntegerField(default=0, null=True, blank=True, verbose_name='온도(*C')
    humidity = models.IntegerField(default=0, null=True, blank=True, verbose_name='습도(%)')
    usegas = models.CharField(max_length=100, null=True, blank=True, verbose_name='가스상태')
    usewater = models.CharField(max_length=100, null=True, blank=True, verbose_name='수도상태')
    alarm = models.CharField(max_length=100, null=True, blank=True, verbose_name='경보내용')
    actgas = models.CharField(max_length=100, null=True, blank=True, verbose_name='가스조치요청')
    actalarm = models.CharField(max_length=100, null=True, blank=True, verbose_name='경보조치요청')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name='참고사항')
    date = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='일시')
    created = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='일시')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

