# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 10:50:13 2018

@author: fangyucheng
"""


import time
import datetime
import requests


def retry_get_url(url, retry_times=3, **kwargs):
    count = 0
    while count < retry_times:
        try:
            get_resp = requests.get(url, **kwargs)
            return get_resp
        except:
            count += 1
            time.sleep(1)
    print('failed to get page %s after %d tries, %s'
          % (url, retry_times, datetime.datetime.now()))
    return None