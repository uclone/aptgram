from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class File(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_files', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1, related_name='group_files', verbose_name='아파트명')
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name='담당부서')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='안건제목')
    abstract = models.TextField(max_length=500, null=True, blank=True, verbose_name='안건요약')
    file = models.FileField(upload_to='files/%Y/%m/%d', null=True, blank=True, verbose_name='품의문서', default='files/aptgram.xlsx')
    approval = models.CharField(max_length=100, verbose_name='결재자(부서:직위:이름)')
    charge = models.CharField(max_length=100, null=True, blank=True, verbose_name='반장비번')
    manager = models.CharField(max_length=100, null=True, blank=True, verbose_name='과장비번')
    director = models.CharField(max_length=100, null=True, blank=True, verbose_name='소장비번')
    board = models.CharField(max_length=100, null=True, blank=True, verbose_name='이사비번')
    super = models.CharField(max_length=100, null=True, blank=True, verbose_name='감사비번')
    visor = models.CharField(max_length=100, null=True, blank=True, verbose_name='회장비번')
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
    author = models.CharField(max_length=100, null=True, blank=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, blank=True, verbose_name='아파트명')
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name='부서')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='안건제목')
    abstract = models.TextField(max_length=500, null=True, blank=True, verbose_name='안건요약')
    approval = models.CharField(max_length=100, verbose_name='결재자(부서:직위:이름)')
    charge = models.CharField(max_length=100, null=True, blank=True, verbose_name='반장비번')
    manager = models.CharField(max_length=100, null=True, blank=True, verbose_name='과장비번')
    director = models.CharField(max_length=100, null=True, blank=True, verbose_name='소장비번')
    board = models.CharField(max_length=100, null=True, blank=True, verbose_name='이사비번')
    super = models.CharField(max_length=100, null=True, blank=True, verbose_name='감사비번')
    visor = models.CharField(max_length=100, null=True, blank=True, verbose_name='회장비번')
    created = models.DateTimeField(blank=True, default=timezone.now)
    updated = models.DateTimeField(blank=True, default=timezone.now)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.file.name

