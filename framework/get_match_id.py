# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 09:59:35 2018

@author: fangyucheng
"""


import argparse
from crawler_opgg.crawler.crawler_user_info import match_id

parse = argparse.ArgumentParser(description='input a user_name to collect')
parse.add_argument('-u', '--user_name', default='goalkeeperfyc', type=str,
                   help=('choose a user to collect match_id'))

args = parse.parse_args()

match_id(user_name=args.user_name,
         table_name='match_info',
         host='172.21.0.17')