# -*- coding: utf-8 -*-
import json
from prettyprint import pp
from random import random
from datetime import date, datetime, timedelta
def randomInterval(l):
    beg = 1
    ret = []
    for i in range(l):
        ret.append(beg * random())
        beg = beg - ret[-1]
    return ret

def genslices():
    t = date.today()
    days = map(lambda x: (t - timedelta(days = x)).strftime('%m-%d'), reversed(range(10)))
    slices = map(lambda x: {'tick': x, 'data': map(lambda x: int(100 * x), randomInterval(4))}, days)
    pp(slices)
    pass

if __name__ == '__main__':
    genslices()
