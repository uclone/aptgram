# Generated by Django 3.0.6 on 2020-06-30 07:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('equipgram', '0011_auto_20200630_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequip',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 6, 30, 7, 2, 17, 25070, tzinfo=utc), null=True, verbose_name='구입일자'),
        ),
    ]