from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tasks', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_tasks', verbose_name='사용목적')
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name='소속')
    charge = models.CharField(max_length=100, null=True, blank=True, verbose_name='담당')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일자')
    subject = models.CharField(max_length=100, verbose_name='제목')
    task = models.TextField(max_length=500, null=True, blank=True, verbose_name='기록내용')
    photo = models.ImageField(upload_to='tasks/%Y/%m/%d', null=True, blank=True, verbose_name='참고', default='tasks/aptgram.jpg')
    manager = models.CharField(max_length=100, null=True, blank=True, verbose_name='관리')
    director = models.CharField(max_length=100, null=True, blank=True, verbose_name='확인')
    updated = models.DateTimeField(auto_now=True, verbose_name='수정일자')
    response = models.CharField(max_length=200, null=True, blank=True, verbose_name='추가사항')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        return reverse('taskgram:task_detail', args=[str(self.id)])


class Stask(models.Model):
    author = models.CharField(max_length=100, null=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='사용목적')
    department = models.CharField(max_length=100, null=True, verbose_name='소속')
    charge = models.CharField(max_length=100, null=True, verbose_name='담당')
    created = models.DateTimeField(null=True, default=timezone.now, verbose_name='작성일자')
    subject = models.CharField(max_length=100, null=True, verbose_name='담당업무')
    task = models.TextField(max_length=500, null=True, verbose_name='기록내용')
    photo = models.ImageField(upload_to='tasks/%Y/%m/%d', null=True, verbose_name='참고', default='tasks/aptgram.jpg')
    manager = models.CharField(max_length=100, null=True, verbose_name='관리')
    director = models.CharField(max_length=100, null=True, verbose_name='확인')
    updated = models.DateTimeField(null=True, default=timezone.now, verbose_name='수정일자')
    response = models.CharField(max_length=200, null=True, blank=True, verbose_name='추가사항')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

