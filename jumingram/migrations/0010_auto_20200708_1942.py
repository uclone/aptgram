# Generated by Django 3.0.6 on 2020-07-08 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumingram', '0009_auto_20200707_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jumin',
            name='task_apt',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='전체 알림'),
        ),
        migrations.AlterField(
            model_name='jumin',
            name='task_dong',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='동별 알림'),
        ),
        migrations.AlterField(
            model_name='jumin',
            name='task_ho',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='개별 알림'),
        ),
    ]
