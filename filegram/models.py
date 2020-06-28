from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse

class File(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_files', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1, related_name='group_files', verbose_name='아파트명')
    department = models.CharField(max_length=100, null=True, verbose_name='담당부서')
    charge = models.CharField(max_length=100, null=True, verbose_name='담당자')
    manager = models.CharField(max_length=100, default='확인 요망', verbose_name='관리자')
    director = models.CharField(max_length=100, default='확인 요망', verbose_name='승인역')
    super = models.CharField(max_length=100, default='확인 요망', verbose_name='추인역')
    subject = models.CharField(max_length=100, null=True, verbose_name='안건제목')
    abstract = models.TextField(max_length=500, default='요약', verbose_name='안건요약')
    file = models.FileField(upload_to='files/%Y/%m/%d', null=True, verbose_name='품의문서', default='files/aptgram.jpg')
    remark = models.CharField(max_length=100, default='없음', verbose_name='비고')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일자')
    updated = models.DateTimeField(auto_now=True, verbose_name='수정일자')

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.file.name

    def get_absolute_url(self):
        return reverse('filegram:file_detail', args=[str(self.id)])

class Sfile(models.Model):
    author = models.CharField(max_length=100, null=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='아파트명')
    department = models.CharField(max_length=100, null=True, verbose_name='부서')
    charge = models.CharField(max_length=100, null=True, verbose_name='담당자')
    manager = models.CharField(max_length=100, default='확인 요망', verbose_name='관리자')
    director = models.CharField(max_length=100, default='확인 요망', verbose_name='승인역')
    super = models.CharField(max_length=100, default='확인 요망', verbose_name='추인역')
    subject = models.CharField(max_length=100, null=True, verbose_name='안건제목')
    abstract = models.TextField(max_length=500, default='요약', verbose_name='안건요약')
    file = models.FileField(upload_to='files/%Y/%m/%d', null=True, verbose_name='품의문서', default='files/aptgram.jpg')
    remark = models.CharField(max_length=100, default='없음', verbose_name='비고')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.file.name

