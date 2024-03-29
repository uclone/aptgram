# Generated by Django 3.0.6 on 2020-06-30 07:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sulbigram', '0010_auto_20200630_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ssulbi',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='작성일자'),
        ),
        migrations.AlterField(
            model_name='ssulbi',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='수정일자'),
        ),
        migrations.AlterField(
            model_name='sulbi',
            name='close',
            field=models.DateField(default=django.utils.timezone.now, null=True, verbose_name='완료일자'),
        ),
        migrations.AlterField(
            model_name='sulbi',
            name='start',
            field=models.DateField(default=django.utils.timezone.now, null=True, verbose_name='시작일자'),
        ),
    ]
