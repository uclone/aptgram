from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Plan(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_plans', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_plans', verbose_name='아파트명')
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name='부서')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='직위/직급')
    regpsw = models.CharField(max_length=100, null=True, blank=True, default='6자리 숫자 또는 영문자(대, 소)', verbose_name='등록비번')
    usepsw = models.CharField(max_length=100, null=True, blank=True, default='자동생성됩니다.',verbose_name='사용비번')
    remark = models.CharField(max_length=200, verbose_name='용도')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일자')
    updated = models.DateTimeField(auto_now=True, verbose_name='발급일자')

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        return reverse('plangram:plan_detail', args=[str(self.id)])


class Splan(models.Model):
    author = models.CharField(max_length=100, null=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='아파트명')
    department = models.CharField(max_length=100, null=True, verbose_name='부서')
    subject = models.CharField(max_length=100, null=True, verbose_name='직위/직급')
    remark = models.CharField(max_length=200, null=True, verbose_name='비고')
    created = models.DateTimeField(blank=True, default=timezone.now, verbose_name='작성일자')
    updated = models.DateTimeField(blank=True, default=timezone.now, verbose_name='발급일자')

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username





