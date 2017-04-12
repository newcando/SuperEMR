# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0005_sccontent_comment_counts'),
    ]

    operations = [
        migrations.AddField(
            model_name='mdluserextinfo',
            name='workday',
            field=models.SmallIntegerField(verbose_name='排班时间', default=1, blank=True),
        ),
        migrations.AlterField(
            model_name='sccomment',
            name='uid',
            field=models.ForeignKey(related_name='scCommentuid_set', to='emr.mdlUserExtInfo'),
        ),
        migrations.AlterField(
            model_name='sccomment',
            name='wid',
            field=models.ForeignKey(related_name='scComment_set', to='emr.scContent'),
        ),
    ]
