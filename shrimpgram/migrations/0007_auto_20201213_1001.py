# Generated by Django 3.0.6 on 2020-12-13 01:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
        ('shrimpgram', '0006_auto_20201110_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shrimp',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_shrimps', to=settings.AUTH_USER_MODEL, verbose_name='업체명'),
        ),
        migrations.AlterField(
            model_name='shrimp',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='작성일시'),
        ),
        migrations.AlterField(
            model_name='shrimp',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_shrimps', to='auth.Group', verbose_name='사용목적'),
        ),
        migrations.AlterField(
            model_name='shrimp',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='구역'),
        ),
        migrations.AlterField(
            model_name='shrimp',
            name='naoh',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='중화제'),
        ),
        migrations.AlterField(
            model_name='shrimp',
            name='serial',
            field=models.CharField(max_length=100, verbose_name='장치번호 또는 식별기호'),
        ),
        migrations.AlterField(
            model_name='sshrimp',
            name='author',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='업체명'),
        ),
        migrations.AlterField(
            model_name='sshrimp',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='작성일시'),
        ),
        migrations.AlterField(
            model_name='sshrimp',
            name='group',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='사용목적'),
        ),
        migrations.AlterField(
            model_name='sshrimp',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='구역'),
        ),
        migrations.AlterField(
            model_name='sshrimp',
            name='naoh',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='중화제'),
        ),
        migrations.AlterField(
            model_name='sshrimp',
            name='serial',
            field=models.CharField(max_length=100, verbose_name='장치번호 또는 식별기호)'),
        ),
    ]