from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class Shrimp(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_shrimps', verbose_name='업체명')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_shrimps', verbose_name='사용목적')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='구역')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='장치종류')
    serial = models.CharField(max_length=100, verbose_name='장치번호 또는 식별기호')
    temp = models.IntegerField(default=0, null=True, blank=True, verbose_name='온도(*C)')
    ph = models.IntegerField(default=0, null=True, blank=True, verbose_name='pH')
    alkali = models.IntegerField(default=0, null=True, blank=True, verbose_name='알칼리도')
    salt = models.IntegerField(default=0, null=True, blank=True, verbose_name='염도(ppm)')
    do = models.IntegerField(default=0, null=True, blank=True, verbose_name='DO(ppm)')
    nh4 = models.IntegerField(default=0, null=True, blank=True, verbose_name='암모니아(ppm)')
    no2 = models.IntegerField(default=0, null=True, blank=True, verbose_name='아질산(ppm)')
    turbid = models.IntegerField(default=0, null=True, blank=True, verbose_name='탁도(ppm)')
    security = models.CharField(max_length=200, null=True, blank=True, verbose_name='보안장치')
    naoh = models.IntegerField(default=0, null=True, blank=True, verbose_name='중화제')
    dang = models.IntegerField(default=0, null=True, blank=True, verbose_name='당밀')
    blower = models.IntegerField(default=0, null=True, blank=True, verbose_name='블로워')
    boiler = models.IntegerField(default=0, null=True, blank=True, verbose_name='보일러')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='특기사항')
    date = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='작성일시')
    xdate = models.DateField(null=True, blank=True, default=timezone.now, verbose_name='수정일시')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='일시')
    mk = models.CharField(max_length=100, null=True, blank=True, verbose_name='구글계정과 동일한 패스워드')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M")

    def get_absolute_url(self):
        return reverse('shrimpgram:shrimp_detail', args=[str(self.id)])


class Sshrimp(models.Model):
    author = models.CharField(max_length=100, null=True, blank=True, verbose_name='업체명')
    group = models.CharField(max_length=100, null=True, blank=True, verbose_name='사용목적')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='구역')
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='장치종류')
    serial = models.CharField(max_length=100, verbose_name='장치번호 또는 식별기호)')
    temp = models.IntegerField(default=0, null=True, blank=True, verbose_name='온도(*C)')
    ph = models.IntegerField(default=0, null=True, blank=True, verbose_name='pH')
    alkali = models.IntegerField(default=0, null=True, blank=True, verbose_name='알칼리도')
    salt = models.IntegerField(default=0, null=True, blank=True, verbose_name='염도(ppm)')
    do = models.IntegerField(default=0, null=True, blank=True, verbose_name='DO(ppm)')
    nh4 = models.IntegerField(default=0, null=True, blank=True, verbose_name='암모니아(ppm)')
    no2 = models.IntegerField(default=0, null=True, blank=True, verbose_name='아질산(ppm)')
    turbid = models.IntegerField(default=0, null=True, blank=True, verbose_name='탁도(ppm)')
    security = models.CharField(max_length=200, null=True, blank=True, verbose_name='보안장치')
    naoh = models.IntegerField(default=0, null=True, blank=True, verbose_name='중화제')
    dang = models.IntegerField(default=0, null=True, blank=True, verbose_name='당밀')
    blower = models.IntegerField(default=0, null=True, blank=True, verbose_name='블로워')
    boiler = models.IntegerField(default=0, null=True, blank=True, verbose_name='보일러')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='특기사항')
    date = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='작성일시')
    xdate = models.DateField(null=True, blank=True, default=timezone.now, verbose_name='수정일시')
    created = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='일시')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username

