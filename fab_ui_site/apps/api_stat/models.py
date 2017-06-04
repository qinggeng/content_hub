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
    path = models.CharField(max_length = 65535, null = False)
    docUrl = models.URLField()
    history = HistoricalRecords()

class TestResult(BaseModel):
    api = models.ForeignKey('ApiEntry', on_delete = models.CASCADE)
    history = HistoricalRecords()
    
