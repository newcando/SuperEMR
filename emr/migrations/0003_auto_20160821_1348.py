# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0002_auto_20160815_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mdlmymedicineeatrecord',
            name='medicine',
            field=models.CharField(max_length=64, verbose_name='药物'),
        ),
    ]
