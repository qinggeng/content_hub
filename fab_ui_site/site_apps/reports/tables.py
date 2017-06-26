# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2 import A
from models import *
from django.utils.safestring import mark_safe

class PerformanceOnTestCaseTable(tables.table):
    class Meta:
        attrs = {'class': 'paleblue', 'style': 'width:100%'}
