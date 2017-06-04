# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2 import A
from models import *
from django.utils.safestring import mark_safe

class DocUrlColumn(tables.Column):
    u"""
    api文档的单元格
    """
    def render(self, value, record):
        docUrl = record.pop('docUrl', u'')
        if len(docUrl) == 0:
            return mark_safe(ur"""<input type='button' value='添加' onclick = 'updateDoc("{p}", "{v}")'/><span>   N/A</span>""".format(p = record['path'], v = docUrl))
        else:
            return mark_safe(ur"""<input type='button' value='修改' onclick = 'updateDoc("{p}", "{v}")'/><a href='{v}' target='_blank'>{v}</a>""".format(p = record['path'], v = docUrl))
        pass

class ApiSummarizeTable(tables.Table):
    class Meta:
        attrs = {'class': 'paleblue', 'style': 'width:100%'}
    path = tables.Column(verbose_name = ur'访问路径')
#    test_passed = tables.Column()
    doc = DocUrlColumn(verbose_name = ur'文档路径', empty_values = ())
    test = tables.Column(verbose_name = ur'测试情况', accessor = A('test'), default = 'N/A')
