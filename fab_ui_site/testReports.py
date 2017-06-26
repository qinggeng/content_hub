# -*- coding: utf-8 -*-
from django.test import Client
import json, re, urlparse, itertools
from datetime import datetime, timedelta
from django.test.testcases import LiveServerTestCase
from site_apps.api_stat.models import TestCase
from prettyprint import pp
class PerformaceReportTest(LiveServerTestCase):
   @classmethod
   def setUpClass(cls):
       from mockTestcases import mocks
       days = {}
       for tcm in mocks:
           tc = TestCase()
           tc.raw_api = ''
           tc.func = tcm['func']
           tc.name = tcm['name']
           tc.author = tcm['author']
           tc.createTime = tcm['createDate']
           tc.save()
           date = tcm['createDate'][:10]
           author = tcm['author']
           if date not in days:
               days[date] = {}
           if author not in days[date]:
               days[date][author] = 0
           days[date][author] += 1
       cls.days = days    
       pass
   @classmethod
   def tearDownClass(cls):
       pass
   def test_individual_performance(self):
       args = {
        'periodType' : 'day',
        'from'       : '2017-06-19',
        'to'         : '2017-06-23'}
       url = '/forms/performanceOnTestcase'
       c = Client()
       resp = c.post(url, json.dumps(args), content_type = 'application/json')
       self.assertEqual(resp.status_code, 302)
       urlPart = urlparse.urlparse(resp.url)
       self.assertTrue(None != re.match(ur'/report/(?P<id>[0-9a-z]+)', urlPart.path))
#       jsonResp = c.get(resp.url, headers = {'Accept': 'application/json'})
#       print jsonResp.content
#       self.assertEqual(jsonResp.status_code, 200)
#       self.assertEqual(resp.content, json.dumps(self.days))
#       jReport = json.loads(jsonResp.content)
       resp = c.get(resp.url+'/page')
       self.assertEqual(resp.status_code, 302)
       print resp.url
       resp = c.get(resp.url, headers = {'Accept': 'text/html'})
       print resp.content
       print resp
       self.assertEqual(resp.status_code, 200)
       with open("static/test/performanceChart.html", 'w') as f:
           f.write(resp.content)
           f.close()

