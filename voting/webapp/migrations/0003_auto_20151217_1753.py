# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20151217_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 17, 53, 12, 111820)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='label',
            name='evidence',
            field=models.ForeignKey(default=0, to='corpus.EvidenceCandidate'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 17, 53, 12, 109328)),
            preserve_default=True,
        ),
    ]
