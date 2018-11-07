# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:12:35 2018

@author: fangyucheng
"""

import requests
import time

start = time.time()
url = 'https://api.github.com/events'
get_page = requests.get(url)
print('Get response from', url)

url2 = 'https://api.github.com/events'
get_page = requests.get(url2)
print('Get response from', url2)

url3 = 'https://api.github.com/events'
get_page = requests.get(url3)
print('Get response from', url3)

url4 = 'https://api.github.com/events'
get_page = requests.get(url4)
print('Get response from', url4)

url5 = 'https://api.github.com/events'
get_page = requests.get(url5)
print('Get response from', url5)

end = time.time()
print('Cost time:', end - start)