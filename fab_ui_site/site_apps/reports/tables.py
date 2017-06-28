# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2 import A
from models import *
from django.utils.safestring import mark_safe

def make_dynamic_column_table_klass(data):
    print data
    attrs = {x: tables.Column() for x in data}
    attrs['Meta'] = type(
            'Meta', 
            (), 
            {
                'attrs': {"class":"paleblue", 'style': "width:100%"}, 
#                "order_by": ("-foo", ) ,
                })
    klass = type('DTable', (tables.Table, ), attrs)
    return klass


class DynamicColumnsMixin(object, ):
#class DynamicColumnsMixin(tables.Table):
    def get_table_class(self):
        print 'call get_table_class'
        print dir(self)
        attrs = dict(foo = tables.Column(), bar = tables.Column())
        attrs['Meta'] = type(
                'Meta', 
                (), 
                {
                    'attrs': {"class":"table"}, 
                    "order_by": ("-foo", ) ,
                    })
        klass = type('DTable', (tables.Table, ), attrs)
        return klass
    def get_table_data(self):
        print 'call get_table_data'
        return self.data
    def __init__(self, data):
        object.__init__(self)
        self.data = data


class PerformanceOnTestCaseTable(DynamicColumnsMixin, tables.SingleTableView):
    class Meta:
        attrs = {'class': 'paleblue', 'style': 'width:100%'}

    def __init__(self, data):
        DynamicColumnsMixin.__init__(self, data)
        tables.SingleTableView.__init__(self)
