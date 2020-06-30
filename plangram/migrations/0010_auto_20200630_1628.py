# Generated by Django 3.0.6 on 2020-06-30 07:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('plangram', '0009_auto_20200630_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='close',
            field=models.DateField(default=django.utils.timezone.now, null=True, verbose_name='완료일자'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='start',
            field=models.DateField(default=django.utils.timezone.now, null=True, verbose_name='시작일자'),
        ),
        migrations.AlterField(
            model_name='splan',
            name='created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='splan',
            name='updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
