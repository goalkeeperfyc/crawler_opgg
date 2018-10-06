# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 13:23:28 2018

@author: goalkeeper
"""



import pymysql


def update_status(update_sql,
                  host='172.21.0.17',
                  user='root',
                  passwd='goalkeeper@1',
                  database_name='crawler_opgg'):
    """
    update status to figure out which record is tested
    """
    connection = pymysql.connect(host=host, user=user, passwd=passwd,
                                 db=database_name, port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute(update_sql)
    connection.commit()
    cursor.close()
    connection.close()
