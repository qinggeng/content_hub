# -*- coding: utf-8 -*-
from django.test import Client
import json
from django.test.testcases import LiveServerTestCase
class ApiTest(LiveServerTestCase):

    def do_create_outline(self):
        args = dict(apiList = """
v2
    auth
        signup
        signin
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
/v2/auth/signup
/v2/auth/signin
/v2/user
/v2/user/:id
""".strip()
        c = Client()
        resp = self.do_create_outline()
        self.assertEqual(resp.content, result)
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
