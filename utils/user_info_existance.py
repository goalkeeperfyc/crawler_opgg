# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 12:25:01 2018

@author: fangyucheng
"""

import pymysql

def existance_in_database(user_name):
    connection = pymysql.connect(host='172.21.0.17', user='root', passwd='goalkeeper@1',
                                 db='crawler_opgg', port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    search_sql = "select * from user_info where user_name='" + user_name + "'"
    existance = cursor.execute(search_sql)
    cursor.close()
    connection.close()
    return existance