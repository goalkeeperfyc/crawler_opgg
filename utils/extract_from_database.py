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


import sys
import logging

#if (2, 7) <= sys.version_info < (3, 2):
# On Python 2.7 and Python3 < 3.2, install no-op handler to silence
# No handlers could be found for logger "elasticsearch" message per
# https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library
#import logging
#logger = logging.getLogger('elasticsearch')
#logger.addHandler(logging.NullHandler())

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
    logger = logging.getLogger('elasticsearch')
    logger.addHandler(NullHandler())