from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse

class Equip(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_equips', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1, related_name='group_equips', verbose_name='아파트명')
    subject = models.CharField(max_length=100, verbose_name='장치명칭')
    location = models.CharField(max_length=100, blank=True, verbose_name='보관장소')
    department= models.CharField(max_length=100, blank=True, verbose_name='관리부서')
    manager_1 = models.CharField(max_length=100, blank=True, verbose_name='관리자(정)')
    manager_2 = models.CharField(max_length=100, blank=True, verbose_name='관리자(부)')
    spec = models.CharField(max_length=100, verbose_name='규격')
    date = models.DateField(blank=True, verbose_name='구입일자')
    photo = models.ImageField(upload_to='equips/%Y/%m/%d', default='equips/aptgram.jpg')
    remark = models.CharField(max_length=200, blank=True, verbose_name='비고')

    class Meta:
        ordering = ['-author']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.photo.name

    def get_absolute_url_file(self):
        return reverse('equipgram:equip_detail', arg=[str(self.id)])


class Sequip(models.Model):
    author = models.CharField(max_length=100, blank=True, verbose_name='작성자')
    group = models.CharField(max_length=100, blank=True, verbose_name='아파트명')
    subject = models.CharField(max_length=100, verbose_name='장치명칭')
    location = models.CharField(max_length=100, blank=True, verbose_name='보관장소')
    department= models.CharField(max_length=100, blank=True, verbose_name='관리부서')
    manager_1 = models.CharField(max_length=100, blank=True, verbose_name='관리자(정)')
    manager_2 = models.CharField(max_length=100, blank=True, verbose_name='관리자(부)')
    spec = models.CharField(max_length=100, verbose_name='규격')
    date = models.DateField(blank=True, verbose_name='구입일자')
    photo = models.ImageField(upload_to='equips/%Y/%m/%d', default='equips/aptgram.jpg')
    remark = models.CharField(max_length=200, blank=True, verbose_name='비고')

    class Meta:
        ordering = ['-author']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.photo.name
