from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Susun(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_susuns', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_susuns', verbose_name='아파트명')
    category = models.CharField(max_length=100, null=True, blank=True, verbose_name='대분류')
    subject = models.CharField(max_length=100, default="대상", verbose_name='대상')
    treatment = models.CharField(max_length=100, null=True, blank=True, verbose_name='공사종별')
    method = models.CharField(max_length=100, null=True, blank=True, verbose_name='공사방법')
    cycle = models.IntegerField(default=0, null=True, blank=True,verbose_name='수선주기(년)')
    ratio = models.IntegerField(default=0, null=True, blank=True,verbose_name='수선율(%)')
    last = models.DateField(blank=True, default=timezone.now, verbose_name='최종수선(년)')
    rule = models.DateField(blank=True, default=timezone.now, verbose_name='법정예정(년)')
    plan = models.DateField(blank=True, default=timezone.now, verbose_name='최종예정(년)')
    cost = models.IntegerField(default=0, null=True, blank=True,verbose_name='수선예정금(원)')
    times = models.IntegerField(default=0, null=True, blank=True,verbose_name='수선예정회수')
    amount = models.IntegerField(default=0, null=True, blank=True,verbose_name='총수선예정금액')
    file = models.FileField(upload_to='susun/%Y/%m/%d', null=True, default='susun/SMK.xlsx', verbose_name='견적서')
    created = models.DateTimeField(auto_now_add=True, verbose_name='최초기안일자')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='최근수정일자')


    class Meta:
        ordering = ['-category', '-subject']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")


    def get_absolute_url(self):
        return reverse('susungram:susun_detail', args=[str(self.id)])


class Ssusun(models.Model):
    author = models.CharField(max_length=100, default="원격검침", verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='아파트명')
    category = models.CharField(max_length=100, null=True, blank=True, verbose_name='대분류')
    subject = models.CharField(max_length=100, default="대상", verbose_name='대상')
    treatment = models.CharField(max_length=100, null=True, blank=True, verbose_name='공사종별')
    method = models.CharField(max_length=100, null=True, blank=True, verbose_name='공사방법')
    cycle = models.IntegerField(default=0, null=True, blank=True,verbose_name='수선주기(년)')
    ratio = models.IntegerField(default=0, null=True, blank=True,verbose_name='수선율(%)')
    last = models.DateField(blank=True, default=timezone.now, verbose_name='최종수선(년)')
    rule = models.DateField(blank=True, default=timezone.now, verbose_name='법정예정(년)')
    plan = models.DateField(blank=True, default=timezone.now, verbose_name='최종예정(년)')
    cost = models.IntegerField(default=0, null=True, blank=True,verbose_name='수선예정금(원)')
    times = models.IntegerField(default=0, null=True, blank=True,verbose_name='수선예정회수')
    amount = models.IntegerField(default=0, null=True, blank=True,verbose_name='총수선예정금액')
    created = models.DateTimeField(auto_now_add=True, verbose_name='최초기안일자')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='최근수정일자')

    class Meta:
        ordering = ['-category', '-subject']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

