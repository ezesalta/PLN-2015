# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='label',
            name='relation_name',
        ),
        migrations.AlterField(
            model_name='choice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 17, 32, 30, 720716)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 17, 32, 30, 718943)),
            preserve_default=True,
        ),
    ]
