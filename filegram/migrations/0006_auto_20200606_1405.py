# Generated by Django 3.0.6 on 2020-06-06 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filegram', '0005_auto_20200603_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='text',
        ),
        migrations.AddField(
            model_name='file',
            name='abstract',
            field=models.TextField(max_length=500, null=True, verbose_name='안건요약'),
        ),
        migrations.AddField(
            model_name='file',
            name='charge',
            field=models.CharField(max_length=50, null=True, verbose_name='책임자'),
        ),
        migrations.AddField(
            model_name='file',
            name='department',
            field=models.CharField(max_length=20, null=True, verbose_name='부서'),
        ),
        migrations.AddField(
            model_name='file',
            name='director',
            field=models.CharField(max_length=50, null=True, verbose_name='승인역'),
        ),
        migrations.AddField(
            model_name='file',
            name='manager',
            field=models.CharField(max_length=50, null=True, verbose_name='부서장'),
        ),
        migrations.AddField(
            model_name='file',
            name='remark',
            field=models.CharField(max_length=100, null=True, verbose_name='비고'),
        ),
        migrations.AddField(
            model_name='file',
            name='subject',
            field=models.CharField(max_length=50, null=True, verbose_name='안건제목'),
        ),
        migrations.AddField(
            model_name='file',
            name='super',
            field=models.CharField(max_length=50, null=True, verbose_name='추인역'),
        ),
        migrations.AlterField(
            model_name='file',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(default='files/aptgram.jpg', null=True, upload_to='files/%Y/%m/%d', verbose_name='품의문서'),
        ),
    ]
