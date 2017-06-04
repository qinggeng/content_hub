# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 11:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_stat', '0003_auto_20170602_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalApiEntry',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updateTime', models.DateTimeField(editable=False, null=True)),
                ('path', models.CharField(max_length=65535)),
                ('docUrl', models.URLField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical api entry',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTestResult',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updateTime', models.DateTimeField(editable=False, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('api', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api_stat.ApiEntry')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical test result',
            },
        ),
    ]
