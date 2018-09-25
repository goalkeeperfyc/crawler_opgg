# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 09:32:41 2018

@author: fangyucheng
"""

import datetime
import pymysql
from crawler_sys.proxy_pool import make_up_sql


def write_lst_into_database(data_lst, table_name, database_name='proxy_pool'):
    """
    write ip address list in mysql database
    """
    connection = pymysql.connect(host='localhost', user='root', passwd='goalkeeper@1',
                                 db=database_name, port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    length = len(data_lst)
    for line in data_lst:
        write_into_sql = make_up_sql.make_up_replace_sql(table_name=table_name, input_dic=line)
        cursor.execute(write_into_sql)

    connection.commit()
    print('write %s pieces of data into database' % length)


def write_dic_into_database(data_dic, table_name, database_name='proxy_pool'):
    """
    write ip address dict in mysql database
    """
    connection = pymysql.connect(host='localhost', user='root', passwd='goalkeeper@1',
                                 db=database_name, port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    write_into_sql = make_up_sql.make_up_replace_sql(table_name=table_name, input_dic=data_dic)
    cursor.execute(write_into_sql)
    connection.commit()
    print('write %s into database' % data_dic['ip_address'])


def extract_raw_data_to_test(create_time=None):
    """
    extract ip address from mysql database to test whether it is useful
    """
    connection = pymysql.connect(host='localhost', user='root', passwd='goalkeeper@1',
                                 db='proxy_pool', port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    if create_time is None:
        create_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    search_sql = "select * from ip_address where create_time <'" + create_time + "' and test_or_not=0"
    cursor.execute(search_sql)
    data_lst = cursor.fetchall()
    return data_lst

def extract_tested_data_to_test(update_time=None):
    """
    extract tested ip address from mysql database to test whether it is useful
    """
    connection = pymysql.connect(host='localhost', user='root', passwd='goalkeeper@1',
                                 db='proxy_pool', port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    if update_time is None:
        update_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    search_sql = "select * from useful_ip where update_time <'" + update_time + "'"
    cursor.execute(search_sql)
    data_lst = cursor.fetchall()
    return data_lst


def extract_data_to_use(update_upper_time=None,
                        update_lower_time=None):
    """
    extract ip address from mysql database to test whether it is useful
    """
    connection = pymysql.connect(host='localhost', user='root', passwd='goalkeeper@1',
                                 db='proxy_pool', port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    if update_upper_time is None:
        update_upper_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    if update_lower_time is None:
        update_lower_time = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(1), '%Y-%m-%d %H:%M:%S')
    search_sql = ("select * from useful_ip where update_time <'" 
                  + update_upper_time + "' and update_time > '"
                  + update_lower_time + "'")
    cursor.execute(search_sql)
    data_lst = cursor.fetchall()
    return data_lst


def update_status(update_dic):
    """
    update status to figure out which record is tested
    """
    connection = pymysql.connect(host='localhost', user='root', passwd='goalkeeper@1',
                                 db='proxy_pool', port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    record_id = update_dic['id']
    update_sql = "update ip_address set test_or_not='1' where (id='" + str(record_id) + "')"
    cursor.execute(update_sql)
    connection.commit()