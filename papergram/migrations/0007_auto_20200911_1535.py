# Generated by Django 3.0.6 on 2020-09-11 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papergram', '0006_auto_20200630_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='file',
            field=models.FileField(blank=True, default='papers/aptgram.xlsx', null=True, upload_to='papers/%Y/%m/%d', verbose_name='문서양식'),
        ),
    ]
