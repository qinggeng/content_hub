# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.
class Page(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    uri = models.CharField(max_length = 65535, null = False)
    content = models.TextField(blank = True)

class PageContributors(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)

class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    #author
    #target
    #time
    #type
    transction = models.TextField(null = False)
