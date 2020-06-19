# Generated by Django 3.0.6 on 2020-06-11 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipgram', '0003_auto_20200608_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sequip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, verbose_name='작성자')),
                ('subject', models.CharField(max_length=100, verbose_name='장치명칭')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='보관장소')),
                ('department', models.CharField(blank=True, max_length=100, verbose_name='관리부서')),
                ('manager_1', models.CharField(blank=True, max_length=100, verbose_name='관리자(정)')),
                ('manager_2', models.CharField(blank=True, max_length=100, verbose_name='관리자(부)')),
                ('spec', models.CharField(max_length=100, verbose_name='규격')),
                ('date', models.DateField(blank=True, verbose_name='구입일자')),
                ('photo', models.ImageField(default='equips/aptgram.jpg', upload_to='equips/%Y/%m/%d')),
                ('remark', models.CharField(blank=True, max_length=200, verbose_name='비고')),
            ],
            options={
                'ordering': ['-author'],
            },
        ),
    ]
