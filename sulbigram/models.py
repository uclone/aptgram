from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse

class Sulbi(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sulbis', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_sulbis', verbose_name='아파트명')
    department = models.CharField(max_length=100, null=True, verbose_name='담당부서')
    subject = models.CharField(max_length=100, null=True, verbose_name='설비명칭')
    action = models.CharField(max_length=100, null=True, verbose_name='관리사항')
    start = models.DateField(null=True, verbose_name='시작일자')
    close = models.DateField(null=True, verbose_name='완료일자')
    text = models.TextField(null=True, max_length=500, verbose_name='관리내역')
    file = models.FileField(upload_to='sulbis/%Y/%m/%d', null=True, default='sulbis/SMK.xlsx', verbose_name='관리문서')
    remark = models.CharField(max_length=100, null=True, verbose_name='비고')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일자')
    updated = models.DateTimeField(auto_now=True, verbose_name='수정일자' )

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.file.name

    def get_absolute_url_file(self):
        return reverse('sulbigram:sulbi_detail', arg=[str(self.id)])


class Ssulbi(models.Model):
    author = models.CharField(max_length=100, null=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, verbose_name='아파트명')
    department = models.CharField(max_length=100, null=True, verbose_name='담당부서')
    subject = models.CharField(max_length=100, null=True, verbose_name='설비명칭')
    action = models.CharField(max_length=100, null=True, verbose_name='관리사항')
    start = models.DateField(null=True, verbose_name='시작일자')
    close = models.DateField(null=True, verbose_name='완료일자')
    text = models.TextField(null=True, max_length=500, verbose_name='관리내역')
    file = models.FileField(upload_to='sulbis/%Y/%m/%d', null=True, default='sulbis/SMK.xlsx', verbose_name='관리문서')
    remark = models.CharField(max_length=100, null=True, verbose_name='비고')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일자')
    updated = models.DateTimeField(auto_now=True, verbose_name='수정일자' )

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.file.name