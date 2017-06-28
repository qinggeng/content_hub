# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from site_apps.api_stat.models import TestCase

from models import *

from views import Chart

def str2date(s):
    return s
    return datetime.strptime(s, '%Y-%m-%d').date()

class PerformanceChart(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(PerformanceChart, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        params = json.loads(request.body)
        if params['periodType'] != 'day':
            return HttpResponse('not supported periodType', status_code = 401)
        fromDate = str2date(params['from'])
        toDate = str2date(params['to'])
        tcs = TestCase.objects.filter(createTime__range = [fromDate, toDate])
        days = {}
        authors = set()
        for tc in tcs:
            d = tc.createTime.date().strftime('%Y-%m-%d')
            a = tc.author
            if a not in authors:
                authors.add(a)
            if d not in days:
                days[d] = {}
            if a not in days[d]:
                days[d][a] = 0
            days[d][a] += 1
        authors = list(authors)
        slices = []
        for day, dayAuthors in days.items():
            slice = {
                'data': [],
                'tick': day,
            }
            for a in authors:
                if a not in dayAuthors:
                    slice['data'].append(0)
                else:
                    slice['data'].append(dayAuthors[a])
            slices.append(slice)
        chartArgs = {
            'chartType': 'stackArea',
            'title': u'个人测试用例增量一览表',
            'xAxis': {'name': u'日期'},
            'yAxis': {'name': u'数量'},
            'series': {'slices': slices, 'style': {'legends': list(authors)}},
        }
        chart = Chart()
        digest = chart.saveChartArg(chartArgs)
        report = Report()
        report.form = request.path
        report.formArgs = request.body
        report.save()
        report.pageUrl = self.makeReportPage(report, digest)
        report.save()
        return HttpResponseRedirect(u'/report/{id}'.format(id = unicode(report.id)))

    def makeReportPage(self, report, digest):
        page = PerformanceOnTestCasePage()
        page.reportId = report
        page.chartArg = digest
        page.save()
        return u'/page/{id}'.format(id = unicode(page.id))
        pass
