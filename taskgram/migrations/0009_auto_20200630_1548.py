# Generated by Django 3.0.6 on 2020-06-30 06:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taskgram', '0008_auto_20200630_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stask',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 30, 6, 48, 13, 691481, tzinfo=utc), null=True, verbose_name='작성일자'),
        ),
        migrations.AlterField(
            model_name='stask',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 30, 6, 48, 13, 691481, tzinfo=utc), null=True, verbose_name='관리일자'),
        ),
    ]
