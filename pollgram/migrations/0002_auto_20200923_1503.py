# Generated by Django 3.0.6 on 2020-09-23 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollgram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='remark',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='비고'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='selection',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='선택'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='remark',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='비고'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='subject',
            field=models.CharField(default=1, max_length=100, verbose_name='투표:선거'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='spoll',
            name='remark',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='비고'),
        ),
    ]
