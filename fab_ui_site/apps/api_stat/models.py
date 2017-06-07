# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
from datetime import datetime
import django.utils.timezone
from simple_history.models import HistoricalRecords

# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    createTime = models.DateTimeField(default = django.utils.timezone.now, editable = False, null = False)
    updateTime = models.DateTimeField(editable = False, null = True)
    def save(self, *args):
        self.updateTime = django.utils.timezone.now()
        models.Model.save(self, *args)

    class Meta:
        abstract = True

class ApiEntry(BaseModel):
    path = models.TextField(null = False)
    docUrl = models.URLField()
    name = models.TextField(default = "")
    history = HistoricalRecords()
    @property
    def testSummary(self):
        template = u"共有{n}个测试用例，经历了{m}轮测试"
        n = len(TestCase.objects.filter(api = self))
        m = len(ApiTestResult.objects.filter(api = self))
        return template.format(n = n, m = m)
    @property
    def passed(self):
        try:
            passed = ApiTestResult.objects.filter(api = self).order_by('updatetime').last().passed
            if passed:
                return u'PASSED'
            else:
                return u'FAILED'
        except Exception, e:
            return u'N/A'


class TestCase(BaseModel):
    api = models.ForeignKey('ApiEntry', on_delete = models.SET_NULL, null = True)
    raw_api = models.TextField(null = False)
    func = models.TextField(null = False)
    name = models.TextField(null = False)
    author = models.TextField(null = False)
    history = HistoricalRecords()

class TestResult(BaseModel):
    api = models.ForeignKey('ApiEntry', on_delete = models.SET_NULL, null = True)
    testRound = models.ForeignKey('TestRound', on_delete = models.CASCADE, null = True)
    testCase = models.ForeignKey('TestCase', on_delete = models.SET_NULL, null = True)
    raw_testcase = models.TextField(null = False, default = '')
    passed = models.BooleanField(null = False, default = False)
    history = HistoricalRecords()

class ApiTestResult(BaseModel):
    api = models.ForeignKey('ApiEntry', on_delete = models.SET_NULL, null = True)
    raw_api = models.TextField(null = False)
    testRound = models.ForeignKey('TestRound', on_delete = models.CASCADE, null = True)
    passed = models.BooleanField(null = False)
    history = HistoricalRecords()
    
class TestRound(BaseModel):
    testtime = models.DateTimeField(editable = False, null = False)
    history = HistoricalRecords()
