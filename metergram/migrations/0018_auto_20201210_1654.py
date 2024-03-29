# Generated by Django 3.0.6 on 2020-12-10 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('metergram', '0017_auto_20201208_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meter',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_meters', to='auth.Group', verbose_name='사용목적'),
        ),
        migrations.AlterField(
            model_name='meter',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='사용장소'),
        ),
        migrations.AlterField(
            model_name='smeter',
            name='group',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='사용목적'),
        ),
        migrations.AlterField(
            model_name='smeter',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='사용장소'),
        ),
    ]
