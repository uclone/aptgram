# Generated by Django 3.0.6 on 2020-09-14 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsgram', '0004_auto_20200911_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='photo',
            field=models.ImageField(blank=True, default='news/aptgram.jpg', null=True, upload_to='news/%Y/%m/%d', verbose_name='알림정보'),
        ),
        migrations.AlterField(
            model_name='snews',
            name='subject',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='공고제목'),
        ),
        migrations.AlterField(
            model_name='snews',
            name='text',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='공고내용'),
        ),
    ]
