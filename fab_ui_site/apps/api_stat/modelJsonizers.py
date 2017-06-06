#-*- coding: utf-8 -*-
from models import *
import json
class ApiEntryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ApiEntry):
            return dict(path = obj.path, id = unicode(obj.id), docUrl = obj.docUrl, updateTime = unicode(obj.updateTime), createTime = unicode(obj.createTime))
        return json.JSONEncoder.default(self, obj)


class TestCaseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TestCase):
            return dict(
                    id = unicode(obj.id), 
                    updateTime = unicode(obj.updateTime), 
                    createTime = unicode(obj.createTime),
                    api = obj.api.path,
                    name = obj.name,
                    func = obj.func,
                    author = obj.author)
        return json.JSONEncoder.default(self, obj)
