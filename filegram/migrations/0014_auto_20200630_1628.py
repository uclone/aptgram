# Generated by Django 3.0.6 on 2020-06-30 07:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('filegram', '0013_auto_20200630_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sfile',
            name='created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sfile',
            name='updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
