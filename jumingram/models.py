from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Jumin(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_jumins')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1, related_name='group_jumins', verbose_name='아파트명')
    dong = models.CharField(max_length=100, null=False, blank=False, verbose_name="동")
    ho = models.CharField(max_length=100, null=False, blank=False, verbose_name="호")
    represent = models.CharField(max_length=100, null=True, blank=True, verbose_name='세대주')
    family = models.CharField(max_length=200, null=True, blank=True, verbose_name='가족정보')
    phone = models.CharField(max_length=100, null=True, blank=True, verbose_name='대표전화')
    car = models.CharField(max_length=100, null=True, blank=True, verbose_name='자동차')
    date = models.DateField(blank=True, default=timezone.now, verbose_name='입주일자')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name='비고')
    photo = models.ImageField(upload_to='jumins/%Y/%m/%d', null=True, blank=True, verbose_name='알림 사진', default='jumins/aptgram.jpg')
    file = models.FileField(upload_to='jumins/%Y/%m/%d', null=True, blank=True, verbose_name='알림 파일', default='jumins/aptgram.jpg')
    task_apt = models.TextField(max_length=300, null=True, blank=True, verbose_name='전체 알림')
    task_dong = models.TextField(max_length=300, null=True, blank=True, verbose_name='동별 알림')
    task_ho = models.TextField(max_length=300, null=True, blank=True, verbose_name='개별 알림')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-dong', '-ho']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.file.name

    def get_absolute_url(self):
        return reverse('jumingram:jumin_detail', args=[str(self.id)])


class Sjumin(models.Model):
    author = models.CharField(max_length=100, null=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='아파트명')
    dong = models.CharField(max_length=100, null=True, verbose_name = "동")
    ho = models.CharField(max_length=100, null=True, verbose_name = "호")
    represent = models.CharField(max_length=100, null=True, verbose_name='세대주')
    family = models.CharField(max_length=200, null=True, verbose_name='가족정보')
    phone = models.CharField(max_length=100, null=True, verbose_name='대표전화')
    car = models.CharField(max_length=100, null=True, verbose_name='자동차')
    date = models.DateField(null=True, verbose_name='입주일자')
    remark = models.CharField(max_length=100, null=True, verbose_name='비고')
    created = models.DateTimeField(blank=True, default=timezone.now)
    updated = models.DateTimeField(blank=True, default=timezone.now)

    class Meta:
        ordering = ['-dong', '-ho']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

#    def __str__(self):
#        return self.file.name
