# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 23:29:06 2018

@author: goalkeeper
"""

import argparse
import pymysql
from crawler_opgg.utils.extract_from_database import extract_data
from crawler_opgg.crawler.crawler_user_info import user_performance

parser = argparse.ArgumentParser(description='get user performance by user id')

parser.add_argument('-sql', '-sql',default='select * from user_info where used=0',
                   type=str, help=('search sql'))

args = parser.parse_args()

connection = pymysql.connect(host='172.21.0.17', 
                             user='root',
                             passwd='goalkeeper@1',
                             db='crawler_opgg',
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

task_lst = extract_data(search_sql=args.sql)
print ('task_lst length is %s' % len(task_lst))

for line in task_lst:
    record_id = line['id']
    user_id = line['user_id']
    user_performance(user_id)
    updata_sql = "update user_info set used=1 where id=" + str(record_id)
    cursor.execute(updata_sql)
    connection.commit()
    print('got %s performance' % user_id)
cursor.close()
connection.close()

