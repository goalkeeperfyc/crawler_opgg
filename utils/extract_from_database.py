# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 19:11:56 2018

@author: fangyucheng
"""

import pymysql

def extract_data(search_sql,
                 sum_of_data=None,
                 host='172.21.0.17',
                 user='root',
                 passwd='goalkeeper@1', 
                 database_name='crawler_opgg',
                 port=3306):

    """
    extract data from mysql
    """
    connection = pymysql.connect(host=host, user=user, passwd=passwd,
                                 db=database_name, port=port,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute(search_sql)
    if sum_of_data is None:
        data_lst = cursor.fetchall()
        return data_lst
    elif sum_of_data is not None:
        data_lst = cursor.fetchall()[:sum_of_data]
        return data_lst