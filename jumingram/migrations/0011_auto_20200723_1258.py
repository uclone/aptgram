# Generated by Django 3.0.6 on 2020-07-23 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jumingram', '0010_auto_20200708_1942'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jumin',
            options={'ordering': ['-dong', '-ho']},
        ),
        migrations.AlterModelOptions(
            name='sjumin',
            options={'ordering': ['-dong', '-ho']},
        ),
    ]