# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 23:29:06 2018

@author: goalkeeper
"""

import argparse
from multiprocessing import Pool
from crawler_opgg.utils.extract_from_database import extract_data
from crawler_opgg.utils.get_data_and_update_status import get_performance_and_update_status


parser = argparse.ArgumentParser(description='get user performance by user id')

parser.add_argument('-s', '--sql',default='select * from user_info where used=0',
                   type=str, help=('search sql'))
parser.add_argument('-p', '--process',default=8, type=int, 
                    help=('the num of process runs simultaneously'))
parser.add_argument('-sum', '--sum', default=None, type=int,
                    help=('the number of match_id extract from database'))

args = parser.parse_args()
pool = Pool(args.process)


task_lst = extract_data(search_sql=args.sql,
                        sum_of_data=args.sum)
print ('task_lst length is %s' % len(task_lst))

for line in task_lst:
    pool.apply_async(get_performance_and_update_status, args=(line,))

pool.close()
pool.join()
