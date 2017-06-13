#-*- coding: utf-8 -*-
import requests, argparse, json
kUpdateApi = u'/api/{id}/testcases'
kDetailApi = u'/api/detail/?path={p}'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", dest = 'host', required = True)
    parser.add_argument("-f", help = "json format testcase list", dest = 'jsonPath', required = True)
    args = parser.parse_args()
    apis = json.load(open(args.jsonPath, 'r'))
    for api in apis:
      print api
      resp = requests.get(args.host + kDetailApi.format(p = api))
      detail = json.loads(resp.content)
      testcases = apis[api]
      resp = requests.post(args.host + kUpdateApi.format(id = detail['id']), json = testcases)
      print resp.content
      print resp
