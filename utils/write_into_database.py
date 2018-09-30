# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 10:45:11 2018

@author: fangyucheng
"""



import pymysql
from crawler_opgg.proxy_pool.make_up_sql import make_up_replace_sql


def write_dic_into_database(data_dic,
                            host='172.21.0.17',
                            user='root',
                            passwd='goalkeeper@1',
                            database_name='crawler_opgg',
                            table_name='user_info'):
    """
    write dict into mysql database
    """
    connection = pymysql.connect(host=host, user=user, passwd=passwd,
                                 db=database_name, port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    write_into_sql = make_up_replace_sql(table_name=table_name, input_dic=data_dic)
    cursor.execute(write_into_sql)
    connection.commit()
    print('write %s into database' % data_dic['ip_address'])


def write_lst_into_database(data_lst, 
                            host='172.21.0.17',
                            user='root',
                            passwd='goalkeeper@1',
                            database_name='crawler_opgg',
                            table_name='user_info'):
    """
    write list into mysql database
    """
    connection = pymysql.connect(host=host, user=user, passwd=passwd,
                                 db=database_name, port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    length = len(data_lst)

    for line in data_lst:
        write_into_sql = make_up_replace_sql(table_name=table_name, input_dic=line)
        cursor.execute(write_into_sql)

    connection.commit()
    print('write %s pieces of data into database' % length)