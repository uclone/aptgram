# Generated by Django 3.0.6 on 2020-09-08 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsgram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='dong',
            field=models.CharField(default='전체', max_length=100, verbose_name='동'),
        ),
        migrations.AlterField(
            model_name='news',
            name='ho',
            field=models.CharField(default='전체', max_length=100, verbose_name='호'),
        ),
    ]
