from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Intro(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_intros')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1, related_name='group_intros',
                              verbose_name='관리처')
    name = models.CharField(max_length=100, default='필수', verbose_name='아파트명')
    metro = models.CharField(max_length=100, default='필수', verbose_name='광역단체명')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='시군구명')
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='세부주소')
    text = models.TextField(max_length=500, null=True, blank=True, verbose_name='상세소개')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='비고')
    view = models.ImageField(upload_to='intros/%Y/%m/%d', null=True, blank=True, verbose_name='아파트전경', default='intros/aptgram.jpg')
    photo = models.ImageField(upload_to='intros/%Y/%m/%d', null=True, blank=True, verbose_name='홍보자료', default='intros/aptgram.jpg')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일자')
    updated = models.DateTimeField(auto_now=True, verbose_name='수정일자')


    class Meta:
        ordering = ['-metro', '-city', '-name']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        return reverse('introgram:intro_detail', args=[str(self.id)])


class Sintro(models.Model):
    name = models.CharField(max_length=100, default='필수', verbose_name='아파트명')
    metro = models.CharField(max_length=100, default='필수', verbose_name='광역단체명')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='시군구명')
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='세부주소')
    text = models.TextField(max_length=500, null=True, blank=True, verbose_name='상세소개')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='비고')

    class Meta:
        ordering = ['-metro', '-city', '-name']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

#    def __str__(self):
#        return self.file.name
