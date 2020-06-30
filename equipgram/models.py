from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone


class Equip(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_equips', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1, related_name='group_equips', verbose_name='아파트명')
    code = models.CharField(max_length=100, null=True, blank=True, verbose_name='비품번호')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='비품명칭')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='보관장소')
    department= models.CharField(max_length=100, null=True, blank=True, verbose_name='관리부서')
    manager_1 = models.CharField(max_length=100, null=True, blank=True, verbose_name='관리자(정)')
    manager_2 = models.CharField(max_length=100, null=True, blank=True, verbose_name='관리자(부)')
    spec = models.CharField(max_length=100, null=True, blank=True, verbose_name='규격')
    date = models.DateField(blank=True, default=timezone.now, verbose_name='구입일자')
    photo = models.ImageField(upload_to='equips/%Y/%m/%d', null=True, blank=True, default='equips/aptgram.jpg')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='비고')

    class Meta:
        ordering = ['-author']

    def __str__(self):
        return self.author.username + " " + self.date.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.photo.name

    def get_absolute_url(self):
        return reverse('equipgram:equip_detail', args=[str(self.id)])
        #return reverse('equipgram:equip_list')

    #def get_absolute_url(self):
    #    return reverse('equipgram:equip_detail', kwargs={'pk': self.pk})


class Sequip(models.Model):
    author = models.CharField(max_length=100, null=True, blank=True, verbose_name='작성자')
    group = models.CharField(max_length=100, null=True, blank=True, verbose_name='아파트명')
    code = models.CharField(max_length=100, null=True, blank=True, verbose_name='비품번호')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='비품명칭')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='보관장소')
    department= models.CharField(max_length=100, null=True, blank=True, verbose_name='관리부서')
    manager_1 = models.CharField(max_length=100, null=True, blank=True, verbose_name='관리자(정)')
    manager_2 = models.CharField(max_length=100, null=True, blank=True, verbose_name='관리자(부)')
    spec = models.CharField(max_length=100, null=True, blank=True, verbose_name='규격')
    date = models.DateField(null=True, blank=True, default=timezone.now, verbose_name='구입일자')
    photo = models.ImageField(upload_to='equips/%Y/%m/%d', null=True, blank=True, default='equips/aptgram.jpg')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='비고')

    class Meta:
        ordering = ['-author']

    def __str__(self):
        return self.author.username + " " + self.date.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.photo.name
