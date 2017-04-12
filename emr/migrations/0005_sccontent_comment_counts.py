# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0004_auto_20160822_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='sccontent',
            name='comment_counts',
            field=models.PositiveIntegerField(verbose_name='评论数', default=0),
        ),
    ]
