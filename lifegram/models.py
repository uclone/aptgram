from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Life(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_lives')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1, related_name='group_lives',
                              verbose_name='아파트명')
    applicant = models.CharField(max_length=100, null=True, verbose_name='신청인(성명:동-호:전화번호)')
    created = models.DateTimeField(auto_now_add=True, verbose_name='민원제기일자')
    subject = models.CharField(max_length=100, default='필수', verbose_name='민원제목')
    task_1 = models.TextField(max_length=500, null=True, blank=True, verbose_name='민원내역')
    photo_1 = models.ImageField(upload_to='lives/%Y/%m/%d', null=True, blank=True, verbose_name='민원사진', default='lives/aptgram.jpg')
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name='담당부서')
    charge = models.CharField(max_length=100, null=True, blank=True, verbose_name='처리담당')
    date = models.DateField(blank=True, default=timezone.now, verbose_name='처리기한')
    close = models.DateField(blank=True, default=timezone.now, verbose_name='처리완료')
    task_2 = models.TextField(max_length=500, null=True, blank=True, verbose_name='처리내역')
    photo_2 = models.ImageField(upload_to='lives/%Y/%m/%d', null=True, blank=True, verbose_name='처리사진', default='lives/aptgram.jpg')
    progress = models.CharField(max_length=200, null=True, blank=True, verbose_name='진행상황')
    response = models.CharField(max_length=200, null=True, blank=True, verbose_name='주민후기')
    open = models.CharField(max_length=200, null=True, blank=True, default='비공개', verbose_name='비공개:공개')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='결재')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

#    def __str__(self):
#        return self.file.name

    def get_absolute_url(self):
        return reverse('lifegram:life_detail', args=[str(self.id)])


class Slife(models.Model):
    author = models.CharField(max_length=100, null=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='아파트명')
    applicant = models.CharField(max_length=100, null=True, verbose_name='신청인(성명:동-호:전화번호)')
    created = models.DateTimeField(blank=True, default=timezone.now, verbose_name='민원제기일자')
    subject = models.CharField(max_length=100, null=True, verbose_name='민원제목')
    task_1 = models.TextField(max_length=500, null=True, verbose_name='민원내역')
    photo_1 = models.ImageField(upload_to='lives/%Y/%m/%d', null=True, verbose_name='민원사진', default='lives/aptgram.jpg')
    department = models.CharField(max_length=100, null=True, verbose_name='처리부서')
    charge = models.CharField(max_length=100, null=True, verbose_name='처리담당')
    date = models.DateField(blank=True, default=timezone.now, verbose_name='처리기한')
    close = models.DateTimeField(blank=True, default=timezone.now, verbose_name='완료일자')
    task_2 = models.TextField(max_length=500, null=True, verbose_name='처리내역')
    photo_2 = models.ImageField(upload_to='lives/%Y/%m/%d', null=True, verbose_name='처리사진', default='lives/aptgram.jpg')
    progress = models.CharField(max_length=200, null=True, blank=True, verbose_name='진행상황')
    response = models.CharField(max_length=200, null=True, blank=True, verbose_name='주민후기')
    open = models.CharField(max_length=200, null=True, blank=True, default='비공개', verbose_name='비공개:공개')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='결재')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

#    def __str__(self):
#        return self.file.name
