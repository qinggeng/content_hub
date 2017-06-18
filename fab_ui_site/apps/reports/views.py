# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe

from models import *

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
    series = map(lambda x: _(name = x, data = [], type = 'line'), legends)
    for slice in args['series']['slices']:
        for s, d in zip(series, slice['data']):
            s['data'].append(d)
    options = _(
        title =  _(text = 'example'),
        tooltip = _(),
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
        return render(request, 'chartPage.html', {'options': mark_safe(json.dumps(echartOptions, ensure_ascii = False))})

    def put(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        args = json.loads(request.body)
        argsStr = json.dumps(args)
        argDigest = digest(argsStr)
        chartArg = ChartArg()
        chartArg.digest = argDigest
        chartArg.content = argsStr
        chartArg.save()
        return HttpResponseRedirect('/report/charts/'+argDigest)
        pass

    def delete(self, request, *args, **kwargs):
        pass
