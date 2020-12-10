# Generated by Django 3.0.6 on 2020-12-10 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskgram', '0014_auto_20201210_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='소속'),
        ),
        migrations.AlterField(
            model_name='task',
            name='subject',
            field=models.CharField(default='dept', max_length=100, verbose_name='제목'),
            preserve_default=False,
        ),
    ]