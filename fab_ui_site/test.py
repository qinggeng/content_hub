# -*- coding: utf-8 -*-
from django.test import Client
import json
from datetime import datetime
from django.test.testcases import LiveServerTestCase
class ApiTest(LiveServerTestCase):

    def do_create_outline(self):
        args = dict(apiList = """
v2
    auth
        signin
        signup
    user
        :id
    """.strip())
        c = Client()
        resp = c.post('/api/outline/', json.dumps(args), content_type = 'application/json')
        return resp

    def test_create_outline(self):
        result = """
/v2
/v2/auth
/v2/auth/signin
/v2/auth/signup
/v2/user
/v2/user/:id
""".strip()
        c = Client()
        resp = self.do_create_outline()
        self.assertEqual(resp.content.strip(), result)
        resp = c.get('/api/outline/')
        self.assertEqual(resp.content, result)
        resp = c.get('/api/outline/v2/user')
        self.assertEqual(resp.content, '/v2/user')

    def test_get_api_detail(self):
        c = Client()
        self.do_create_outline()
        resp = c.get('/api/detail?path=/v2/user')
        self.assertEqual(resp.status_code, 200)
        d = json.loads(resp.content)
        self.assertEqual(d['path'], '/v2/user')
        
    def test_update_api_detail_doc(self):
        self.do_create_outline()
        c = Client()
        args = dict(path = '/v2/user', docUrl = 'http://www.bing.com')
        resp = c.post('/api/detail', json.dumps(args), content_type = 'application/json')
        self.assertEqual(resp.status_code, 200)
        api = json.loads(resp.content)
        self.assertEqual(args['docUrl'], api['docUrl'])
        resp = c.get('/api/detail?path=/v2/user')
        self.assertEqual(resp.status_code, 200)
        api = json.loads(resp.content)
        self.assertEqual(args['docUrl'], api['docUrl'])

    def test_update_api_detail_history(self):
        self.do_create_outline()
        c = Client()
        args = dict(path = '/v2/user', docUrl = 'http://www.bing.com')
        resp = c.post('/api/detail', json.dumps(args), content_type = 'application/json')
        self.assertEqual(resp.status_code, 200)
        api = json.loads(resp.content)
        self.assertEqual(args['docUrl'], api['docUrl'])
        resp = c.get('/api/{id}/history'.format(id = api['id']))
        self.assertEqual(resp.status_code, 200)

    def test_get_api_summary(self):
        self.do_create_outline()
        c = Client()
        args = dict(path = '/v2/user', docUrl = 'http://www.bing.com')
        resp = c.post('/api/detail', json.dumps(args), content_type = 'application/json')
        resp = c.get('/api/summary')
        self.assertEqual(resp.status_code, 200)
        with open('static/test/test.html', 'w') as f:
            f.write(resp.content)
            f.close()

    def do_create_testcase(self, testcases = None):
        c = Client()
        resp = c.get('/api/detail?path=/v2/user')
        self.assertEqual(resp.status_code, 200)
        detail = json.loads(resp.content)
        if None == testcases:
            testcases = [dict(name = 'aaa', func = 'bbb', author = 'hyk')]
        resp = c.post('/api/{id}/testcases'.format(id = detail['id']), json.dumps(testcases), content_type = 'application/json')
        self.assertEqual(resp.status_code, 200)
        detail = json.loads(resp.content)
        return (detail, c)

    def test_append_api_testcase(self):
        n1 = datetime.now()
        self.do_create_outline()
        testcases = [dict(name = 'aaa', func = 'bbb', author = 'hyk')]
        detail, c = self.do_create_testcase(testcases)
        testcase = detail[0]
        self.assertTrue('api' in testcase)
        self.assertEqual(testcases[0]['name'], testcase['name'])
        self.assertEqual(testcases[0]['func'], testcase['func'])
        self.assertEqual(testcases[0]['author'], testcase['author'])
        resp = c.get('/api/detail?path=/v2/user')
        self.assertEqual(resp.status_code, 200)
        detail = json.loads(resp.content)
        resp = c.get('/api/{id}/testcases'.format(id = detail['id']))
        self.assertEqual(resp.status_code, 200)
        detail = json.loads(resp.content)
        self.assertEqual(len(detail), 1)
        testcase = detail[0]
        self.assertTrue('api' in testcase)
        self.assertEqual(testcases[0]['name'], testcase['name'])
        self.assertEqual(testcases[0]['func'], testcase['func'])
        self.assertEqual(testcases[0]['author'], testcase['author'])
        n2 = datetime.now()
        print (n2 - n1).total_seconds()

    def test_append_test_round(self):
        self.do_create_outline()
        detail, c = self.do_create_testcase()
        args = dict(epoch = int(datetime.now().strftime('%s')),
                test_results = [dict(api = '/v2/user',
                    passed = True,
                    func = 'bbb')])
        resp = c.post('/api/test_round/', json.dumps(args), content_type = 'application/json')
        self.assertEqual(resp.status_code, 200)
        detail = json.loads(resp.content)
        self.assertTrue('id' in detail)
        resp = c.get('/api/detail?path=/v2/user')
        self.assertEqual(resp.status_code, 200)
        detail = json.loads(resp.content)
        self.assertTrue('testSummary' in detail)
        print detail['testSummary']
        self.assertEqual(u'共有1个测试用例, 经历了1轮测试', detail['testSummary'])
        self.assertTrue('testResult' in detail)
        self.assertEqual('PASSED', detail['testResult'])
