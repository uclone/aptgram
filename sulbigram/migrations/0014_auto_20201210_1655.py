# Generated by Django 3.0.6 on 2020-12-10 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('sulbigram', '0013_auto_20200911_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ssulbi',
            name='department',
            field=models.CharField(max_length=100, null=True, verbose_name='담당'),
        ),
        migrations.AlterField(
            model_name='ssulbi',
            name='group',
            field=models.CharField(max_length=100, null=True, verbose_name='사용목적'),
        ),
        migrations.AlterField(
            model_name='ssulbi',
            name='remark',
            field=models.CharField(max_length=100, null=True, verbose_name='확인'),
        ),
        migrations.AlterField(
            model_name='sulbi',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='담당'),
        ),
        migrations.AlterField(
            model_name='sulbi',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_sulbis', to='auth.Group', verbose_name='사용목적'),
        ),
        migrations.AlterField(
            model_name='sulbi',
            name='remark',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='확인'),
        ),
    ]
