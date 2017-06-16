# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import json
from datetime import datetime
from hashlib import md5
from time import ctime

def digest(text):
    m = md5()
    m.update(text)
    return m.hexdigest()


class Chart(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Chart, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        args = json.loads(request.body)
        argDigest = digest(json.dumps(args))
        return HttpResponseRedirect('/report/charts/'+argDigest)
        pass

    def delete(self, request, *args, **kwargs):
        pass
