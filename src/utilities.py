#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   utils.py
@Time    :   2022/11/07 21:18:24
@Author  :   Xin Dong
@Contact :   xindong9511@gmail.com
@License :   (C)Copyright 2020-2022, XinDong
'''

import os
import sys
import datetime
import time
import random
import urllib

def add_time(func):
    def wrapper(*args, **kw):
        time_now = time.strftime("%Y-%m-%d %H:%M:%S")
        sys.stdout.write(f'[ INFO {time_now} ] ')
        return func(*args, **kw)
    return wrapper

@add_time
def print_log(string, end="\n"):
    print(string, end=end)

def convert_time(timeRegion):
    """check input time region and split per 31 days
    """
    minString = timeRegion.split('-')[0]
    maxString = timeRegion.split('-')[1]
    t1, t2 = minString.split('/'), maxString.split('/')
    mintime = datetime.datetime(int(t1[0]), int(t1[1]), int(t1[2]))
    maxtime = datetime.datetime(int(t2[0]), int(t2[1]), int(t2[2]))
    deltTime = maxtime - mintime
    getSplitTime = []
    if deltTime > datetime.timedelta(days=31):
        cnt = int(str(deltTime).split(' ')[0]) / 31
        for i in range(1, cnt+2):
            if i == 1:
                start = mintime
                mintime = start + datetime.timedelta(days=31)
                getSplitTime.append(
                    '%s-%s' % (start.strftime("%Y/%m/%d"), mintime.strftime("%Y/%m/%d")))
            elif i > 1 and i <= cnt:
                start = mintime + datetime.timedelta(days=1)
                mintime = start + datetime.timedelta(days=31)
                getSplitTime.append(
                    '%s-%s' % (start.strftime("%Y/%m/%d"), mintime.strftime("%Y/%m/%d")))
            else:
                start = mintime + datetime.timedelta(days=1)
                getSplitTime.append(
                    '%s-%s' % (start.strftime("%Y/%m/%d"), maxtime.strftime("%Y/%m/%d")))
         # output record to log file, so that user known what happened
        print_log("# the input date region include %s" % str(deltTime))
        print_log("# split date region into %d:" % len(getSplitTime))
        for i in getSplitTime:
            print_log(i)
        return getSplitTime
    return [timeRegion]

def GDSid_to_Acc(gdsId):
    """Given a GDS id, e.g. 300982523, tries to give a GDS accession, e.g.
    GSM982523

    NOTE: there is an algorithm: 1 - GPL; 2 - GSE; 3 - GSM;
    acc = "GSM"+gdsId[1:] (strip leading 0s)
    """
    #Cut = dropping of the "3" (which indicates sample) and removal of leading
    #leading 0s
    cut = gdsId[1:].lstrip("0")
    if gdsId[0] == '1':
        typ = 'GPL'
    elif gdsId[0] == '2':
        typ = 'GSE'
    elif gdsId[0] == '3':
        typ = 'GSM'
    else:
        raise Exception('NotMatchGEOTypeError')
    return f"{typ}{cut}"


def proxyInstead(link, using=False):
    """using proxy to aviod forbidden
    """
    context = ''
    if using:
        # using proxy first
        try:  # using proxy first, or using the read ip
            agent = [x.rstrip() for x in open('./pickle_file/proxy.txt')]
            proxy = {'http': 'http://%s' % random.sample(agent, 1)[0]}
            urlf = urllib.request.urlopen(link, proxies=proxy)
            print_log('.')
        except:
            urlf = urllib.request.urlopen(link)
            proxy = {'proxy': 'local IP'}
            # use for record, so that we can know what happened if error occured
            print_log('.')
        # check whether we get the correct inf
        context = urlf.read()
        urlf.close()
        if ('404 - File or directory not found' in context) or ('ERR_ACCESS_DENIED' in context) or (context.strip() == ''):
            urlf = urllib.request.urlopen(link)
            context = urlf.read()
            urlf.close()
            proxy = {'proxy': 'local IP'}
            print_log('.')
        print_log('%s: %s' % (list(proxy.values())[0], link))
        context = context.decode(encoding='utf-8', errors='ignore')
        return context
    try:
        # time.sleep(0.3)
        urlf = urllib.request.urlopen(link)
        context = urlf.read()
        context = context.decode(encoding='utf-8', errors='ignore')
        urlf.close()
        print_log('local IP: %s' % link)
        return context
    except:
        print('link problem: %s' % link)
    return None

