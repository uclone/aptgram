# Generated by Django 3.0.6 on 2020-09-11 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumingram', '0012_auto_20200827_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='jumin',
            name='note',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='비고'),
        ),
        migrations.AddField(
            model_name='sjumin',
            name='note',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='비고'),
        ),
        migrations.AlterField(
            model_name='jumin',
            name='remark',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='결재'),
        ),
    ]
