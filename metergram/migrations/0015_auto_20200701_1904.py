# Generated by Django 3.0.6 on 2020-07-01 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metergram', '0014_auto_20200630_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meter',
            name='ho',
            field=models.CharField(default='호', max_length=100, verbose_name='호'),
        ),
    ]
