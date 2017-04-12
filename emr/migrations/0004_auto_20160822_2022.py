# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0003_auto_20160821_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='scComment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('ctext', models.CharField(max_length=1000, verbose_name='文字内容', default='')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('uid', models.ForeignKey(to='emr.mdlUserExtInfo')),
            ],
            options={
                'verbose_name': '用户动态',
                'ordering': ['-time'],
                'verbose_name_plural': '用户动态',
            },
        ),
        migrations.CreateModel(
            name='scContent',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000, verbose_name='文字内容', default='')),
                ('img1', models.FileField(null=True, upload_to='SC/%Y/%m/%d', verbose_name='图片1', blank=True)),
                ('img2', models.FileField(null=True, upload_to='SC/%Y/%m/%d', verbose_name='图片2', blank=True)),
                ('img3', models.FileField(null=True, upload_to='SC/%Y/%m/%d', verbose_name='图片3', blank=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('uid', models.ForeignKey(to='emr.mdlUserExtInfo')),
            ],
            options={
                'verbose_name': '用户动态',
                'ordering': ['-time'],
                'verbose_name_plural': '用户动态',
            },
        ),
        migrations.CreateModel(
            name='scMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000, verbose_name='文字内容', default='')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('uid', models.ForeignKey(related_name='mdlUserExtInfo_uid_set', to='emr.mdlUserExtInfo')),
                ('uid2', models.ForeignKey(related_name='mdlUserExtInfo_uid2_set', to='emr.mdlUserExtInfo')),
            ],
            options={
                'verbose_name': '用户动态',
                'ordering': ['-time'],
                'verbose_name_plural': '用户动态',
            },
        ),
        migrations.AddField(
            model_name='sccomment',
            name='wid',
            field=models.ForeignKey(to='emr.scContent'),
        ),
    ]
