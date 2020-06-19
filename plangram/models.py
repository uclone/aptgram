from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse

class Plan(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_plans', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_plans', verbose_name='아파트명')
    start = models.DateField(null=True, verbose_name='시작일자')
    close = models.DateField(null=True, verbose_name='완료일자')
    department = models.CharField(max_length=50, null=True, verbose_name='담당부서')
    charge = models.CharField(max_length=50, null=True, verbose_name='담당자')
    subject = models.CharField(max_length=50, null=True, verbose_name='업무제목')
    task = models.TextField(max_length=500, null=True, verbose_name='업무내역')
    photo = models.ImageField(upload_to='plans/%Y/%m/%d', null=True, verbose_name='참고사진', default='plans/aptgram.jpg')
    manager = models.CharField(max_length=50, null=True, verbose_name='업무관리')
    director = models.CharField(max_length=50, null=True, verbose_name='책임관리')
    remark = models.CharField(max_length=200, null=True, verbose_name='비고')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.photo.name

    def get_absolute_url_file(self):
        return reverse('plangram:plan_detail', arg=[str(self.id)])


class Splan(models.Model):
    author = models.CharField(max_length=50, null=True, verbose_name='작성자')
    group = models.CharField(max_length=50, null=True, verbose_name='아파트명')
    start = models.DateField(null=True, verbose_name='시작일자')
    close = models.DateField(null=True, verbose_name='완료일자')
    department = models.CharField(max_length=50, null=True, verbose_name='담당부서')
    charge = models.CharField(max_length=50, null=True, verbose_name='담당자')
    subject = models.CharField(max_length=50, null=True, verbose_name='업무제목')
    task = models.TextField(max_length=500, null=True, verbose_name='업무내역')
    photo = models.ImageField(upload_to='plans/%Y/%m/%d', null=True, verbose_name='참고사진', default='plans/aptgram.jpg')
    manager = models.CharField(max_length=50, null=True, verbose_name='업무관리')
    director = models.CharField(max_length=50, null=True, verbose_name='책임관리')
    remark = models.CharField(max_length=200, null=True, verbose_name='비고')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.photo.name