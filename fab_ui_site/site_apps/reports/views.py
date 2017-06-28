# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from prettyprint import pp

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe

from models import *
from tables import make_dynamic_column_table_klass

# Create your views here.
import json
from datetime import datetime
from hashlib import md5
from time import ctime

def digest(text):
    m = md5()
    m.update(text)
    return m.hexdigest()

def makeEchartOptions(args):
    _ = dict
    xAxis = map(lambda x: x['tick'], args['series']['slices'])
    legends = args['series']['style']['legends']
    label = _(normal = _(show = False, position = 'top'))
    series = map(lambda x: _(name = x, stack = u"总量", areaStyle = _(normal = _()), label = label, data = [], type = 'line'), legends)
    for slice in args['series']['slices']:
        for s, d in zip(series, slice['data']):
            s['data'].append(d)
    tooltip = _(
        trigger = 'axis',
        axisPointer = _(
            type = 'cross',
            label = _(
                backgoundColor = '#6a7985')))
    options = _(
        title =  _(text = args.get('title', u'无标题图表')),
        tooltip = tooltip,
        legend = _(data = legends),
        xAxis = _(data = xAxis),
        yAxis = _(),
        series = series
    )
    return options



class Chart(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Chart, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        digest = kwargs.pop("id")
        chartArg = ChartArg.objects.get(digest = digest)
        chartArg = json.loads(chartArg.content)
        echartOptions = makeEchartOptions(chartArg)
        return render(request, 'chartPage.html', {'title': echartOptions['title']['text'], 'options': mark_safe(json.dumps(echartOptions, ensure_ascii = False))})

    def put(self, request, *args, **kwargs):
        pass

    def saveChartArg(self, args):
        argsStr = json.dumps(args)
        argDigest = digest(argsStr)
        try:
            return ChartArg.objects.get(digest = argDigest).digest
        except Exception, e:
            pass
        chartArg = ChartArg()
        chartArg.digest = argDigest
        chartArg.content = argsStr
        chartArg.save()
        return argDigest


    def post(self, request, *args, **kwargs):
        args = json.loads(request.body)
        argDigest = self.saveChartArg(args)
        return HttpResponseRedirect('/report/charts/'+argDigest)
        pass

    def delete(self, request, *args, **kwargs):
        pass

class ReportView(View):
    def get(self, request, *args, **kwargs):
        pass

class ReportPage(View):
    def get(self, request, *args, **kwargs):
        reportId = kwargs.pop("id")
        try:
            report = Report.objects.get(id = reportId)
            if report.pageUrl != None:
                return HttpResponseRedirect(report.pageUrl)
            else:
                return HttpResponse('report page not found', status = 404)
        except Exception, e:
            return HttpResponse('report not found', status = 404)

class PageView(View):
    def renderPerformanceOnTestCasePage(self):
        pass
    def get(self, request, *args, **kwargs):
        pageId = kwargs.pop("id")
        try:
            page = Page.objects.get(id = pageId).performanceontestcasepage
            if None == page:
                return HttpResponse('page not found', status = 404)
            chartArgs = json.loads(ChartArg.objects.get(digest = page.chartArg).content)
            slices = chartArgs['series']['slices']
            legends = chartArgs['series']['style']['legends']
            tableData = reduce(
                    lambda x, y: map(lambda a: x[a[0]] + [a[1]], enumerate(y)), 
                    map(lambda x: x['data'], slices), 
                    map(lambda x: [], range(len(slices[0]['data']))))
            columns = map(lambda x: x['tick'], slices)
            columns = ['NA'] + columns
            tableData = map(lambda x: [x[0]] + x[1], zip(legends, tableData))
            tableData = map(lambda x: dict(zip(columns, x)), tableData)
            tableKlass = make_dynamic_column_table_klass(columns)
            chartOptions = makeEchartOptions(chartArgs)

            return render(
                    request, 
                    'performanceOnTestCase.html', 
                    {'performanceOnTestCase': tableKlass(tableData),
                        'chartOptions': mark_safe(json.dumps(chartOptions, ensure_ascii = False))})
            return HttpResponse('not implement yet', status = 500)
        except Exception, e:
            raise
            return HttpResponse('page not found', status = 404)
