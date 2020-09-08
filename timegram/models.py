from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone


class Time(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_times', verbose_name='작성자')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_times', verbose_name='아파트명')
    subject = models.CharField(max_length=200, default='업무', verbose_name='업무')
    description = models.TextField(max_length=500, null=True, blank=True, default='상세내용', verbose_name='상세내용')
    remark = models.CharField(max_length=100, null=True, blank=True, default='비고', verbose_name='비고')
    action = models.CharField(max_length=100, null=True, blank=True, default='저장', verbose_name='일정편집')
    start_time = models.DateField(verbose_name='시작일자', default=timezone.now)
    end_time = models.DateField(verbose_name='종료일자', default=timezone.now)

    @property
    def get_html_url(self):
        url = reverse('timegram:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.subject} </a>'
