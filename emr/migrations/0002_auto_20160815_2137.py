# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mdluserextinfo',
            name='user_type',
            field=models.CharField(null=True, default='A', max_length=4, blank=True, verbose_name='用户类型'),
        ),
    ]
