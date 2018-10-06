# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 23:29:06 2018

@author: goalkeeper
"""

import argparse
from multiprocessing import Pool
from crawler_opgg.utils.extract_from_database import extract_data
from crawler_opgg.crawler.crawler_user_info import user_performance
from crawler_opgg.utils.update_status_in_mysql import update_status


parser = argparse.ArgumentParser(description='get user performance by user id')

parser.add_argument('-s', '--sql',default='select * from user_info where used=0',
                   type=str, help=('search sql'))
parser.add_argument('-p', '--process',default=8, type=int, 
                    help=('the num of process runs simultaneously'))
parser.add_argument('-sum', '--sum', default=None, type=int,
                    help=('the number of match_id extract from database'))

args = parser.parse_args()
pool = Pool(args.process)

def get_performance_and_update_status(user_info_dic):
    record_id = user_info_dic['id']
    user_id = user_info_dic['user_id']
    user_performance(user_id)
    update_sql = "update user_info set used=1 where id=" + str(record_id)
    update_status(update_sql)
    print('got %s performance' % user_id)
 
task_lst = extract_data(search_sql=args.sql,
                        sum_of_data=args.sum)
print ('task_lst length is %s' % len(task_lst))

for line in task_lst:
    pool.apply_async(get_performance_and_update_status, args=(line,))

pool.close()
pool.join()
