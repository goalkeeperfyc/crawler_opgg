# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 14:11:54 2018

@author: fangyucheng
"""

from crawler_opgg.utils.extract_from_database import extract_data

search_sql = "select * from user_performance"

data_lst = extract_data(search_sql, host='cdb-1y1l8q6e.bj.tencentcdb.com',
                        port=10037)