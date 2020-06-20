# Generated by Django 3.0.6 on 2020-06-20 03:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipgram', '0005_auto_20200615_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equip',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_equips', to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
        ),
    ]
