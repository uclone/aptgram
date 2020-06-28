from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse

class Life(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_lives')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1, related_name='group_lives',
                              verbose_name='아파트명')
    contact = models.CharField(max_length=100, default="신청인의 주소, 연락처 기재", verbose_name='신청인')
    created = models.DateTimeField(auto_now_add=True, verbose_name='민원제기일자')
    subject = models.CharField(max_length=100, null=True, verbose_name='민원제목')
    task_1 = models.TextField(max_length=500, null=True, verbose_name='민원내역')
    photo_1 = models.ImageField(upload_to='lives/%Y/%m/%d', null=True, verbose_name='민원사진',
                                default='lives/aptgram.jpg')
    charge = models.CharField(max_length=100, null=True, verbose_name='처리담당')
    updated = models.DateTimeField(auto_now=True, verbose_name='응답&처리일자')
    department = models.CharField(max_length=100, null=True, verbose_name='처리부서')
    task_2 = models.TextField(max_length=500, null=True, verbose_name='처리내역')
    photo_2 = models.ImageField(upload_to='lives/%Y/%m/%d', null=True, verbose_name='처리사진',
                                default='lives/aptgram.jpg')
    response = models.CharField(max_length=200, default="처리결과에 대한 평가", verbose_name='민원평가')

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

#    def __str__(self):
#        return self.file.name

    def get_absolute_url(self):
        return reverse('lifegram:life_detail', args=[str(self.id)])


class Slife(models.Model):
    author = models.CharField(max_length=100, null=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='아파트명')
    contact = models.CharField(max_length=100, verbose_name='신청인')
    created = models.DateTimeField(auto_now_add=True, verbose_name='민원제기일자')
    subject = models.CharField(max_length=100, null=True, verbose_name='민원제목')
    task_1 = models.TextField(max_length=500, null=True, verbose_name='민원내역')
    photo_1 = models.ImageField(upload_to='lives/%Y/%m/%d', null=True, verbose_name='민원사진',
                                default='lives/aptgram.jpg')
    charge = models.CharField(max_length=100, null=True, verbose_name='처리담당')
    updated = models.DateTimeField(auto_now=True, verbose_name='응답&처리일자')
    department = models.CharField(max_length=100, null=True, verbose_name='처리부서')
    task_2 = models.TextField(max_length=500, null=True, verbose_name='처리내역')
    photo_2 = models.ImageField(upload_to='lives/%Y/%m/%d', null=True, verbose_name='처리사진',
                                default='lives/aptgram.jpg')
    response = models.CharField(max_length=200, default="처리결과에 대한 평가", verbose_name='민원평가')

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

#    def __str__(self):
#        return self.file.name
