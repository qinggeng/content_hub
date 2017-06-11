# -*- coding: utf-8 -*-
"""
测试脚本使用方法：
# 将runner改为ReportRunner
# 运行
"""
from django.test.runner import DiscoverRunner
from unittest import TestResult, TextTestRunner
import re, os, os.path

class JsonTestResult(TestResult):
    pattern = re.compile(ur'(?P<method>[a-zA-Z_][a-zA-Z_0-9]*)\s*\((?P<clsName>[^\)]+)\)')
    propPattern = re.compile(ur'^@(?P<name>[^=]+)\s*=\s*(?P<val>.*$)')
    def __init__(self, rawResults):
        super(JsonTestResult, self).__init__()
        self.rawResults = rawResults

    def addError(self, test, err):
        super(JsonTestResult, self).addError(test, err)

    def addfailure(self, test, fail):
        super(jsontestresult, self).addfailure(test, fail)

    def addSuccess(self, test):
        m = self.pattern.match(unicode(test))
        attrName = m.group('method')
        className = m.group('clsName')
        if hasattr(test, attrName):
            doc = getattr(test, attrName).__doc__
            if None != doc:
                props = {}
                for line in doc.split('\n'):
                    m = self.propPattern.match(line)
                    if m:
                        props[m.group('name')] = m.group('val')
                try:
                    self.rawResults.append(dict(
                        api = props['api'],
                        func = className + '.' + attrName,
                        passed = True))
                except Exception, e:
                    print e
                    pass
        super(JsonTestResult, self).addSuccess(test)

class LowLevelRunner(TextTestRunner):
    def __init__(self, *args, **kwargs):
        super(LowLevelRunner, self).__init__(*args, **kwargs)
        try:
            import testConfig
        except Exception, e:
            print e
            pass
        self.rawResults = []

    def _makeResult(self):
        self._result = JsonTestResult(self.rawResults)
        return self._result

    def run(self, test):
        ret = super(LowLevelRunner, self).run(test)
        #todo aggrate a report?
        print self.rawResults
        return ret

class ReportRunner(DiscoverRunner):
    test_runner = LowLevelRunner
    def __init__(self, pattern='test*.py', top_level=None, verbosity=1, interactive=True, failfast=False, keepdb=False, reverse=False, debug_sql=False, **kwargs):
        DiscoverRunner.__init__(self, pattern='test*.py', top_level=None, verbosity=1, interactive=True, failfast=False, keepdb=False, reverse=False, debug_sql=False, **kwargs)
