# Generated by Django 3.0.6 on 2020-06-28 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plangram', '0004_auto_20200620_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='close',
            field=models.DateField(default='2020-06-28', null=True, verbose_name='완료일자'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='start',
            field=models.DateField(default='2020-06-28', null=True, verbose_name='시작일자'),
        ),
    ]
