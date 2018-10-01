# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 09:59:35 2018

@author: fangyucheng
"""


import argparse
from crawler_opgg.crawler.crawler_user_info import match_id
from crawler_opgg.utils.extract_from_database import extract_data


parse = argparse.ArgumentParser(description='extract user name from database and get match_id by user name')
parse.add_argument('-s', '--sum', default=20, type=int,
                   help=('the sum of user name to use'))

args = parse.parse_args()

search_sql = 'select user_name from user_info order by create_time desc'

task_lst = extract_data(search_sql=search_sql,
                        sum_of_data=args.sum)

for line in task_lst:
    user_name = line['user_name']
    try:
        match_id(user_name=user_name,
                 table_name='match_info',
                 host='172.21.0.17')
    except:
        print("can't get match_id by %s" % user_name)