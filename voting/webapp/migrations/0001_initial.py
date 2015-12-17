# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0017_auto_20150302_1916'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 12, 17, 17, 32, 0, 9922))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('relation_name', models.CharField(default='', max_length=30)),
                ('label', models.BooleanField(default=0)),
                ('evidence', models.ForeignKey(default=0, to='corpus.EvidenceCandidate', unique=True)),
                ('relation', models.ForeignKey(to='corpus.Relation', default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField(max_length=300)),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 12, 17, 17, 32, 0, 8276))),
                ('law', models.ForeignKey(to='corpus.Entity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vote', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='choice',
            name='choice',
            field=models.ForeignKey(to='webapp.Vote'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='webapp.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='choice',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=0),
            preserve_default=True,
        ),
    ]
