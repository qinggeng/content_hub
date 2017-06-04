# -*- coding: utf-8 -*-
import re

def genApis(apiDoc):
    scope_char = ""
    scope_count = 0
    prefix = ''
    indent = 0
    prefices = {0:''}
    pattern = re.compile(ur'(?P<scope>\s*)(?P<name>[0-9a-zA-Z:-]*)')
    entries = []
    for line in apiDoc.split('\n'):
        m = pattern.match(line)
        if None != m:
            scopes = m.group('scope')
            node = m.group('name')
            if "" == scope_char:
                scope_char = scopes
            if "" != scope_char:
                indent = len(scopes) / len(scope_char)
            entry = prefices[indent] + '/' + node
            entries.append(entry)
            prefices[indent + 1] = entry
    return entries
