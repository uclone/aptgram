# Generated by Django 3.0.6 on 2020-06-29 05:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taskgram', '0006_auto_20200620_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stask',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 29, 5, 25, 43, 818368, tzinfo=utc), null=True, verbose_name='작성일자'),
        ),
        migrations.AlterField(
            model_name='stask',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 29, 5, 25, 43, 819364, tzinfo=utc), null=True, verbose_name='관리일자'),
        ),
    ]
