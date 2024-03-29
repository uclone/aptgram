# Generated by Django 3.0.6 on 2020-09-14 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sintro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='필수', max_length=100, verbose_name='아파트명')),
                ('metro', models.CharField(default='필수', max_length=100, verbose_name='광역단체명')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='시군구명')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='세부주소')),
                ('text', models.TextField(blank=True, max_length=500, null=True, verbose_name='상세소개')),
                ('remark', models.CharField(blank=True, max_length=200, null=True, verbose_name='비고')),
            ],
            options={
                'ordering': ['-metro', '-city', '-name'],
            },
        ),
        migrations.CreateModel(
            name='Intro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='필수', max_length=100, verbose_name='아파트명')),
                ('metro', models.CharField(default='필수', max_length=100, verbose_name='광역단체명')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='시군구명')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='세부주소')),
                ('text', models.TextField(blank=True, max_length=500, null=True, verbose_name='상세소개')),
                ('remark', models.CharField(blank=True, max_length=200, null=True, verbose_name='비고')),
                ('view', models.ImageField(blank=True, default='intros/aptgram.jpg', null=True, upload_to='intros/%Y/%m/%d', verbose_name='아파트전경')),
                ('photo', models.ImageField(blank=True, default='intros/aptgram.jpg', null=True, upload_to='intros/%Y/%m/%d', verbose_name='홍보자료')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='작성일자')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_intros', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='group_intros', to='auth.Group', verbose_name='관리처')),
            ],
            options={
                'ordering': ['-metro', '-city', '-name'],
            },
        ),
    ]
