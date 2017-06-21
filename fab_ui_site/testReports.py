# -*- coding: utf-8 -*-
from django.test import Client
import json, re, urlparse
from datetime import datetime, timedelta
from django.test.testcases import LiveServerTestCase
from apps.api_stat.models import TestCase
class PerformaceReportTest(LiveServerTestCase):
   @classmethod
   def setUpClass(cls):
       authors = ['John', 'Mike', 'Frank']
       dates = map(lambda x: datetime.strptime('2017-06-19', '%Y-%m-%d') + timedelta(days = x), range(5))
       
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
       self.assertTrue(None != re.atch(ur'/reports/(?P<id>[0-9a-z]+)'))
       jsonResp = c.get(resp.url, headers = {'Accept': 'application/json'})
       self.assertEqual(resp.status_code, 200)
       jReport = json.loads(jsonResp.content)
       hResp = c.get(resp.url, headers = {'Accept': 'text/html'})
       with open("static/test/performanceChart.html", 'w') as f:
           f.write(hResp.content)
           f.close()

