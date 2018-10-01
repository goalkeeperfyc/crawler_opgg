# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 11:20:27 2018

@author: fangyucheng
"""

import argparse
import multiprocessing
import pymysql
from crawler_opgg.crawler.crawler_user_info import user_info
from crawler_opgg.utils.extract_from_database import extract_data


connection = pymysql.connect(host='172.21.0.17', user='root', passwd='goalkeeper@1',
                                 db='crawler_opgg', port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

parser = argparse.ArgumentParser(description='input variable')

parser.add_argument('-p', '--process', default=5, type=int,
                    help=('the num of process'))
parser.add_argument('-host', '--host', default='172.21.0.17', type=str,
                    help=('host of the database writing data into'))
parser.add_argument('-sql', '--sql', default="select * from match_info where used=0", type=str,
                    help=('set search_sql to extract data'))
parser.add_argument('-sum', '--sum', default=None, type=str,
                    help=('the number of match_id extract from database'))

args = parser.parse_args()

data_lst = extract_data(search_sql=args.sql,
                        sum_of_data=args.sum)
print('totally found %s matches' % len(data_lst))

for line in data_lst:
    record_id = line['id']
    match_id = line['match_id']
    process = multiprocessing.Process(targer=user_info, args=(match_id, ))
    process.start()
    updata_sql = "update match_info set used=1 where id=" + str(record_id)
    cursor.execute(updata_sql)
    connection.commit()    
    cursor.close()
    connection.close()

