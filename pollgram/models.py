import datetime
from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Poll(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_polls', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_polls', verbose_name='아파트명')
    subject = models.CharField(max_length=100, verbose_name='투표:선거')
    pub_date = models.DateTimeField(verbose_name='공개일자')
    open_date = models.DateTimeField(verbose_name='개시일시')
    close_date = models.DateTimeField(verbose_name='마감일시')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='비고')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일자')
    updated = models.DateTimeField(auto_now=True, verbose_name='정정일자')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_absolute_url(self):
        return reverse('pollgram:poll_detail', args=[str(self.id)])

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name='투표:선거')
    selection = models.CharField(max_length=200, null=True, blank=True, verbose_name='선택')
    votes = models.IntegerField(default=0, verbose_name='투표수')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='비고')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일자')
    updated = models.DateTimeField(auto_now=True, verbose_name='정정일자')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        return reverse('pollgram:poll_detail', args=[str(self.id)])


class Spoll(models.Model):
    author = models.CharField(max_length=100, null=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='아파트명')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='투표:선거')
    pub_date = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='공개일자')
    open_date = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='개시일시')
    close_date = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='마감일시')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='비고')
    created = models.DateTimeField(blank=True, default=timezone.now, verbose_name='작성일자')
    updated = models.DateTimeField(blank=True, default=timezone.now, verbose_name='정정일자')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.author.username

