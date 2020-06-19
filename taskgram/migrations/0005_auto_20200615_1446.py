# Generated by Django 3.0.6 on 2020-06-15 05:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taskgram', '0004_auto_20200612_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='stask',
            name='group',
            field=models.CharField(max_length=50, null=True, verbose_name='아파트명'),
        ),
        migrations.AddField(
            model_name='task',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='group_tasks', to='auth.Group', verbose_name='아파트명'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tasks', to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
        ),
    ]
