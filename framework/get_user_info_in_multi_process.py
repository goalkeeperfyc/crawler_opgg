# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 11:20:27 2018

@author: fangyucheng
"""

import argparse
import pymysql
from multiprocessing import Pool
from crawler_opgg.utils.extract_from_database import extract_data
from crawler_opgg.utils.get_data_and_update_status import get_info_and_update_status

connection = pymysql.connect(host='172.21.0.17', user='root', passwd='goalkeeper@1',
                                 db='crawler_opgg', port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

parser = argparse.ArgumentParser(description='input variable')

parser.add_argument('-p', '--process', default=8, type=int,
                    help=('the num of process runs simultaneously'))
parser.add_argument('-host', '--host', default='172.21.0.17', type=str,
                    help=('host of the database writing data into'))
parser.add_argument('-sql', '--sql', default="select * from match_info where used=0", type=str,
                    help=('set search_sql to extract data'))
parser.add_argument('-sum', '--sum', default=None, type=int,
                    help=('the number of match_id extract from database'))

args = parser.parse_args()

data_lst = extract_data(search_sql=args.sql,
                        sum_of_data=args.sum)
print('totally found %s matches' % len(data_lst))

pool = Pool(args.process)

for line in data_lst:
    pool.apply_async(get_info_and_update_status, args=(line, ))

pool.close()
pool.join()

