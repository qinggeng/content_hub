#-*- coding: utf-8 -*-
from models import *
import json
class ApiEntryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ApiEntry):
            return dict(path = obj.path, id = unicode(obj.id), docUrl = obj.docUrl, updateTime = unicode(obj.updateTime), createTime = unicode(obj.createTime))
        return json.JSONEncoder.default(self, obj)
