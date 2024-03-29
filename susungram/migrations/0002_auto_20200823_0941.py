# Generated by Django 3.0.6 on 2020-08-23 00:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('susungram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='susun',
            name='last',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='최종수선(년)'),
        ),
        migrations.AlterField(
            model_name='susun',
            name='plan',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='최종예정(년)'),
        ),
        migrations.AlterField(
            model_name='susun',
            name='rule',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='법정예정(년)'),
        ),
    ]
