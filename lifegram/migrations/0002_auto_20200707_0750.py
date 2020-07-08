# Generated by Django 3.0.6 on 2020-07-06 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifegram', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='life',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='life',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='slife',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='slife',
            name='last_name',
        ),
        migrations.AddField(
            model_name='life',
            name='applicant',
            field=models.CharField(max_length=100, null=True, verbose_name='신청인'),
        ),
        migrations.AddField(
            model_name='slife',
            name='applicant',
            field=models.CharField(max_length=100, null=True, verbose_name='신청인'),
        ),
    ]
