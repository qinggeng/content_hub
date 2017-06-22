# -*- coding: utf-8 -*-
import json, itertools
from prettyprint import pp
from random import random, Random, choice
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

def genTestcases():
   authors = ['John', 'Mike', 'Frank']
   dates = map(lambda x: datetime.strptime('2017-06-19', '%Y-%m-%d') + timedelta(days = x), range(5))
   r = Random()
   seq = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
   k = (reduce(lambda x, y: x + map(lambda z: {'author': y[0], 'createDate': y[1], 'func':reduce(lambda x, y: x + choice(seq), range(13), ''), 'name':reduce(lambda x, y: x + choice(seq), range(10), '') }, range(r.randint(5, 30))), itertools.product(authors, dates), []))
   pp(k)
       

if __name__ == '__main__':
    #genslices()
    genTestcases()
