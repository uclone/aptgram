from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_news')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1, related_name='group_news', verbose_name='아파트명')
    dong = models.CharField(max_length=100, null=False, default='전체', blank=False, verbose_name="동")
    ho = models.CharField(max_length=100, null=False, default='전체', blank=False, verbose_name="호")
    date = models.DateField(blank=True, default=timezone.now, verbose_name='공고일자')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='공고제목')
    text = models.TextField(max_length=300, null=True, blank=True, verbose_name='공고내용')
    file = models.FileField(upload_to='news/%Y/%m/%d', null=True, blank=True, verbose_name='공고파일', default='news/aptgram.xlsx')
    photo = models.ImageField(upload_to='news/%Y/%m/%d', null=True, blank=True, verbose_name='알림정보', default='news/aptgram.jpg')
    remark = models.CharField(max_length=100, null=True, blank=True, default='결재', verbose_name='결재')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.file.name

    def get_absolute_url(self):
        return reverse('newsgram:news_detail', args=[str(self.id)])


class Snews(models.Model):
    author = models.CharField(max_length=100, null=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='아파트명')
    dong = models.CharField(max_length=100, null=True, verbose_name = "동")
    ho = models.CharField(max_length=100, null=True, verbose_name = "호")
    date = models.DateField(blank=True, default=timezone.now, verbose_name='공고일자')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='공고제목')
    text = models.TextField(max_length=300, null=True, blank=True, verbose_name='공고내용')
    remark = models.CharField(max_length=100, null=True, blank=True, default='기안', verbose_name='기안:승인')
    created = models.DateTimeField(blank=True, default=timezone.now, verbose_name='작성일')
    updated = models.DateTimeField(blank=True, default=timezone.now, verbose_name='결재일')

    class Meta:
        ordering = ['-date', '-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")