# Generated by Django 3.0.6 on 2020-06-20 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifegram', '0004_auto_20200615_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='life',
            name='charge',
            field=models.CharField(max_length=100, null=True, verbose_name='처리담당'),
        ),
        migrations.AlterField(
            model_name='life',
            name='contact',
            field=models.CharField(default='신청인의 주소, 연락처 기재', max_length=100, verbose_name='신청인'),
        ),
        migrations.AlterField(
            model_name='life',
            name='department',
            field=models.CharField(max_length=100, null=True, verbose_name='처리부서'),
        ),
        migrations.AlterField(
            model_name='life',
            name='subject',
            field=models.CharField(max_length=100, null=True, verbose_name='민원제목'),
        ),
        migrations.AlterField(
            model_name='slife',
            name='author',
            field=models.CharField(max_length=100, null=True, verbose_name='작성자'),
        ),
        migrations.AlterField(
            model_name='slife',
            name='charge',
            field=models.CharField(max_length=100, null=True, verbose_name='처리담당'),
        ),
        migrations.AlterField(
            model_name='slife',
            name='contact',
            field=models.CharField(max_length=100, verbose_name='신청인'),
        ),
        migrations.AlterField(
            model_name='slife',
            name='department',
            field=models.CharField(max_length=100, null=True, verbose_name='처리부서'),
        ),
        migrations.AlterField(
            model_name='slife',
            name='group',
            field=models.CharField(max_length=100, null=True, verbose_name='아파트명'),
        ),
        migrations.AlterField(
            model_name='slife',
            name='subject',
            field=models.CharField(max_length=100, null=True, verbose_name='민원제목'),
        ),
    ]
