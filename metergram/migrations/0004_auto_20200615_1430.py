# Generated by Django 3.0.6 on 2020-06-15 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metergram', '0003_auto_20200615_1427'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meter',
            old_name='author',
            new_name='xauthor',
        ),
    ]
