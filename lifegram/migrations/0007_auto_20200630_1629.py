# Generated by Django 3.0.6 on 2020-06-30 07:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lifegram', '0006_auto_20200630_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slife',
            name='created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='민원제기일자'),
        ),
    ]