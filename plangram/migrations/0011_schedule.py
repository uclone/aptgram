# Generated by Django 3.0.6 on 2020-07-23 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plangram', '0010_auto_20200630_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(null=True, verbose_name='시작일자')),
                ('close', models.DateField(null=True, verbose_name='완료일자')),
                ('department', models.CharField(max_length=100, null=True, verbose_name='담당부서')),
                ('subject', models.CharField(max_length=100, null=True, verbose_name='업무제목')),
                ('remark', models.CharField(max_length=200, null=True, verbose_name='비고')),
            ],
        ),
    ]
