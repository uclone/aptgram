# Generated by Django 3.0.6 on 2020-06-29 05:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('equipgram', '0007_auto_20200628_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equip',
            name='date',
            field=models.DateField(blank=True, default='2020-06-29', verbose_name='구입일자'),
        ),
        migrations.AlterField(
            model_name='sequip',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 6, 29, 5, 25, 43, 824351, tzinfo=utc), verbose_name='구입일자'),
        ),
    ]
