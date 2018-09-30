# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 09:36:55 2018

@author: fangyucheng
"""


import pymysql
from crawler_opgg.utils.write_into_database import write_lst_into_database

connection = pymysql.connect(host='172.21.0.17', 
                             user='root',
                             passwd='goalkeeper@1',
                             db='crawler_opgg', 
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

search_sql = "select * from user_info"
cursor.execute(search_sql)

test_lst = cursor.fetchall()

new_lst = []
user_id_lst = []
for line in test_lst:
    if line['user_id'] not in user_id_lst:
        new_lst.append(line)
        user_id_lst.append(line['user_id'])

delect_sql = "delect from user_info where id >= 1"
cursor.execute(delect_sql)
connection.commit()

write_lst_into_database(data_lst=test_lst,
                        table_name='user_info',
                        host='172.21.0.17')