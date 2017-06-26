# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
import django.utils.timezone
from simple_history.models import HistoricalRecords

# Create your models here.
class Page(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    uri = models.TextField(max_length = 65535, null = True)
    pageClass = models.TextField(max_length = 65535, null = True)
    history = HistoricalRecords()
    def save(self, *args):
        pageClass = type(self).__name__
        models.Model.save(self, *args)
#    class Meta:
#        abstract = True

class PerformanceOnTestCasePage(Page):
    reportId = models.ForeignKey('Report', on_delete = models.SET_NULL, null = True)
    chartArg = models.TextField(null = True)

class PageContributors(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    history = HistoricalRecords()

class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    #author
    #target
    #time
    #type
    transction = models.TextField(null = False)
    history = HistoricalRecords()

class Chart(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    args = models.TextField()
    history = HistoricalRecords()

class ChartArg(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    digest = models.TextField(blank = True)
    content = models.TextField(default = u"")
    history = HistoricalRecords()

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    form = models.TextField(null = False)
    formArgs = models.TextField(null = False)
    pageUrl = models.URLField(null = True)
    history = HistoricalRecords()

