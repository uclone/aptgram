# Generated by Django 3.0.6 on 2020-06-15 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('jumingram', '0007_auto_20200613_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='jumin',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='group_jumins', to='auth.Group'),
        ),
    ]
