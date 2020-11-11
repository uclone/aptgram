from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

class KospiPredict(models.Model):
    date = models.DateField("날짜", max_length=10, null=False, unique=True)
    close = models.FloatField("종가", null=True)
    open = models.FloatField("시가", null=True)