# Generated by Django 3.0.6 on 2020-12-14 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metergram', '0019_meter_mk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meter',
            name='mk',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='구글계정과 동일한 패스워드'),
        ),
    ]