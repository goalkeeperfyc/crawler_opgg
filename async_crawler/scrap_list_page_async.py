# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 10:40:12 2018

@author: fangyucheng
"""


"""
This is a framework for async crawler.
Currently, it is for v_qq only
"""


import argparse
import asyncio
import configparser
from multiprocessing import Pool

arg_parser = argparse.ArgumentParser(description='')

arg_parser.add_argument('-p', '--platform', default=[], action='append',
                        help=('input platform names, they will be assembled in python list.'))
arg_parser.add_argument('-c', '--channel', default=[], action='append',
                        help=('if you want to get special list page input the channel, nor all channels will be catched'))

args = arg_parser.parse_args()

if args.platform == []:
    platform_lst = ['腾讯视频']
else:
    platform_lst = args.platfrom

target_lst_page = configparser.ConfigParser()
target_lst_page.read('D:/python_code/crawler/crawler_sys/utils/target_list_page.ini')

task_lst = []

for platfrom in platform_lst:
    lst_page_dic = target_lst_page[platfrom]
    if 
    for key, value in lst_page_dic.items():
        task_lst.append(value)
