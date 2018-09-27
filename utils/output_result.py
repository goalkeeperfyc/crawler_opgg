# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 10:50:13 2018

@author: fangyucheng
"""


import pymysql
from crawler_opgg.utils.trans_format import dic_lst_to_file
from crawler_opgg.proxy_pool.make_up_sql import make_up_replace_sql


def output_to_mysql(result_lst, table_name,
                    host='localhost',
                    user='fangyucheng',
                    passwd='goalkeeper@1',
                    port=3306,
                    database_name='crawler_opgg'):
    connection = pymysql.connect(host=host,
                                 user=user,
                                 passwd=passwd,
                                 port=port,
                                 db=database_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    for line in result_lst:
        replace_sql = make_up_replace_sql(table_name=table_name,
                                          input_dic=line)
        cursor.execute(replace_sql)
        connection.commit()
    print('write %s records into database' % len(result_lst))


def output_result(result_lst,
                  output_to_mysql=True,
                  table_name='user_info',
                  output_to_file=False,
                  file_name=None):

    if output_to_mysql is True and table_name is not None:
        output_to_mysql(result_lst=result_lst,
                        table_name=table_name)

    if output_to_file is True and file_name is not None:
        dic_lst_to_file(lst_name=result_lst,
                        file_name=file_name)
    else:
        pass
