# Generated by Django 3.0.6 on 2020-06-30 06:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('metergram', '0010_auto_20200630_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smeter',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 6, 30, 6, 46, 57, 694705, tzinfo=utc), verbose_name='검침일자'),
        ),
    ]