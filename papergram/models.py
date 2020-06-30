from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Paper(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_papers', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_papers', verbose_name='소유자')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='양식제목')
    file = models.FileField(upload_to='papers/%Y/%m/%d', null=True, blank=True, default='papers/SMK.xlsx', verbose_name='문서양식')
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name='양식설명')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        return reverse('papergram:paper_detail', args=[str(self.id)])


class Spaper(models.Model):
    author = models.CharField(max_length=100, null=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='소유자')
    subject = models.CharField(max_length=100, null=True, verbose_name='양식제목')
    file = models.FileField(upload_to='papers/%Y/%m/%d', null=True, default='papers/SMK.xlsx', verbose_name='문서양식')
    description = models.TextField(max_length=500, null=True, verbose_name='양식설명')
    created = models.DateTimeField(blank=True, default=timezone.now)
    updated = models.DateTimeField(blank=True, default=timezone.now)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.photo.name