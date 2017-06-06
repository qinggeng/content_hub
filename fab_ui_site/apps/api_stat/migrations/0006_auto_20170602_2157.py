# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 21:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_stat', '0005_auto_20170605_0644'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalTestCase',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updateTime', models.DateTimeField(editable=False, null=True)),
                ('raw_api', models.TextField()),
                ('func', models.TextField()),
                ('name', models.TextField()),
                ('author', models.TextField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('api', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api_stat.ApiEntry')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical test case',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTestRound',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updateTime', models.DateTimeField(editable=False, null=True)),
                ('testtime', models.DateTimeField(editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical test round',
            },
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updateTime', models.DateTimeField(editable=False, null=True)),
                ('raw_api', models.TextField()),
                ('func', models.TextField()),
                ('name', models.TextField()),
                ('author', models.TextField()),
                ('api', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_stat.ApiEntry')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestRound',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updateTime', models.DateTimeField(editable=False, null=True)),
                ('testtime', models.DateTimeField(editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='historicaltestresult',
            name='raw_testcase',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='testresult',
            name='raw_testcase',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='api',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_stat.ApiEntry'),
        ),
        migrations.AddField(
            model_name='historicaltestresult',
            name='testCase',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api_stat.TestCase'),
        ),
        migrations.AddField(
            model_name='historicaltestresult',
            name='testRound',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api_stat.TestRound'),
        ),
        migrations.AddField(
            model_name='testresult',
            name='testCase',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_stat.TestCase'),
        ),
        migrations.AddField(
            model_name='testresult',
            name='testRound',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_stat.TestRound'),
        ),
    ]
