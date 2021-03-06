# Generated by Django 3.0.6 on 2020-06-12 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskgram', '0003_auto_20200607_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50, null=True, verbose_name='작성자')),
                ('department', models.CharField(max_length=50, null=True, verbose_name='소속부서')),
                ('charge', models.CharField(max_length=50, null=True, verbose_name='담당자')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='작성일자')),
                ('subject', models.CharField(max_length=50, null=True, verbose_name='담당업무')),
                ('task', models.TextField(max_length=500, null=True, verbose_name='업무내역')),
                ('photo', models.ImageField(default='tasks/aptgram.jpg', null=True, upload_to='tasks/%Y/%m/%d', verbose_name='참고')),
                ('manager', models.CharField(max_length=50, null=True, verbose_name='관리자')),
                ('director', models.CharField(max_length=50, null=True, verbose_name='승인역')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='관리일자')),
                ('response', models.CharField(default='관리자 또는 승인자 입력', max_length=200, null=True, verbose_name='업무평가')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AlterField(
            model_name='task',
            name='director',
            field=models.CharField(max_length=50, null=True, verbose_name='승인역'),
        ),
    ]
