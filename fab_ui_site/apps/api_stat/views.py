# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db import transaction

import json

from models import ApiEntry, TestCase
from utils import genApis
from modelJsonizers import *
from tables import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from time import ctime
from datetime import datetime
# Create your views here.



class ApiOutline(View):
    def get(self, request, *args, **kwargs):
        apiPath = kwargs.pop("api", "")
        if "/" == apiPath:
            apis = map(lambda x: x.path, ApiEntry.objects.all())
        else:
            apis = map(lambda x: x.path, ApiEntry.objects.filter(path = apiPath))
        apis.sort()
        return HttpResponse('\n'.join(apis), status = 200)
    def put(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        args = json.loads(request.body)
        apiList = args['apiList']
        apis = genApis(apiList)
        for api in apis:
            try:
                ApiEntry.objects.get(path = api)
                continue
            except Exception, e:
                pass
            entry = ApiEntry(path = api)
            entry.save()

        return HttpResponse('\n'.join(apis), status = 200)
        pass
    def delete(self, request, *args, **kwargs):
        pass

class ApiDetail(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ApiDetail, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        apiPath = request.GET['path']
        if None == apiPath:
            return HttpResponse("missing path in request", status = 401)
        apis = ApiEntry.objects.filter(path = apiPath)
        if len(apis) == 0:
            return HttpResponse(ur'apidoc for "{p}" not found'.format(p = apiPath), status = 404)
        api = apis[0]
        return HttpResponse(json.dumps(api, cls = ApiEntryEncoder), content_type='application/json', status = 200)
        pass

    def put(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        args = json.loads(request.body)
        apis = ApiEntry.objects.filter(path = args['path'])
        if len(apis) == 0:
            apis = []
            apis.append(ApiEntry())
        api = apis[0]
        for key in filter(lambda x: x not in set(['id', 'createTime', 'updateTime']), args.keys()):
            if 'name' == key:
                args[key] = args[key]
            if hasattr(api, key):
                setattr(api, key, args[key])
        api.save()
        return HttpResponse(json.dumps(api, cls = ApiEntryEncoder), content_type='application/json', status = 200)
        pass

    def delete(self, request, *args, **kwargs):
        pass

class ApiSummary(View):
    def get(self, request, *args, **kwargs):
        apis = ApiEntry.objects.all().order_by('path')
        apis = map(lambda x: dict(path = x.path, docUrl = x.docUrl, id = x.id, name = x.name, passed = x.passed, testSummary = x.testSummary), apis)
        return render(request, 'apiList.html', {'api': ApiSummarizeTable(apis)})

class ApiHistory(View):
    def get(self, request, *args, **kwargs):
        apiId = kwargs.pop('id')
        api = ApiEntry.objects.get(id = apiId)
        return HttpResponse(json.dumps(map(lambda x: x.instance, api.history.all()), cls = ApiEntryEncoder), status = 200)

class ApiTestCase(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ApiTestCase, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        apiId = kwargs.pop('id')
        try:
            api = ApiEntry.objects.get(id = apiId)
        except Exception, e:
            return HttpResponse(u'bad request, api "{id}" dose not exist'.format(id = apiId), status = 404)
        testcases = TestCase.objects.filter(api = api)
        return HttpResponse(json.dumps(list(testcases), cls = TestCaseEncoder), status = 200)

    def post(self, request, *args, **kwargs):
        args = json.loads(request.body)
        apiId = kwargs.pop('id')
        try:
            api = ApiEntry.objects.get(id = apiId)
        except Exception, e:
            return HttpResponse(u'bad request, api "{}" dose not exist'.format(apiId), status = 404)
        for testcase in args:
            name = testcase['name']
            func = testcase['func']
            author = testcase['author']
            tc = TestCase(name = name, func = func, author = author, api = api, raw_api = api.path)
            tc.save()
        testcases = TestCase.objects.filter(api = api)
        return HttpResponse(json.dumps(list(testcases), cls = TestCaseEncoder), status = 200)

class ApiTestRound(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            args = json.loads(request.body)
        except Exception, e:
            return HttpResponse('invalid request body', status = 401)
        apiResults = {}
        testRound = TestRound()
        testRound.testtime = datetime.fromtimestamp(args['epoch'])
        testRound.save()
        testResults = args['test_results']
        for testResult in testResults:
            apiPath = testResult['api']
            passed = testResult['passed']
            func = testResult['func']
            apiResult = None
            if apiPath not in apiResults:
                try:
                    api = ApiEntry.objects.get(path = apiPath)
                    apiResult = ApiTestResult(api = api, testRound = testRound, raw_api = api.path, passed = testResult['passed'])
                    apiResults[apiPath] = apiResult
                    apiResult.save()
                except Exception, e:
                    #TODO logging
                    print 'REQUEST ERROR: unknown api path: {p}'.format(apiPath)
                    continue
            else:
                apiResult = apiResults[apiPath]
                apiResult.passed = (apiResult.passed and testResult['passed'])
                apiResult.save()
            testResultRecord = TestResult(api = apiResult.api, testRound = testRound, testCase = TestCase.objects.get(func = testResult['func']), raw_testcase = testResult['func'], passed = testResult['passed'])
            testResultRecord.save()
        return HttpResponse(json.dumps(testRound, cls = TestRoundEncoder), status = 200)


