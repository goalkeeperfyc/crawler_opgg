# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 11:20:27 2018

@author: fangyucheng
"""

import argparse
import pymysql
from crawler_opgg.crawler.crawler_user_info import user_info


parser = argparse.ArgumentParser(description='input variable')

parser.add_argument('-host', '--host', default='172.21.0.17', type=str,
                    help=('host of the database writing data into'))

args = parser.parse_args()

connection = pymysql.connect(host=args.host, 
                             user='root',
                             passwd='goalkeeper@1',
                             db='crawler_opgg',
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

search_sql = "select * from match_info where used=0"
cursor.execute(search_sql)
data_lst = cursor.fetchall()
print('totally found %s matches' % len(data_lst))
for line in data_lst:
    record_id = line['id']
    match_id = line['match_id']
    user_info(match_id=match_id,
              host=args.host)
    updata_sql = "updata match_info set used=1 where id=" + str(record_id)
    cursor.execute(updata_sql)
    connection.commit()
    
cursor.close()
connection.close()