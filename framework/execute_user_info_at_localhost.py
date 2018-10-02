# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 09:12:36 2018

@author: goalkeeper
"""


from crawler_opgg.crawler.crawler_user_info import user_info_at_localhost
from crawler_opgg.utils.trans_format import dic_lst_to_file
from crawler_opgg.utils.extract_from_database import extract_data

search_sql = "select * from match_info where used=0 order by create_time asc"

task_lst = extract_data(search_sql,
                        sum_of_data=10,
                        host='cdb-1y1l8q6e.bj.tencentcdb.com',
                        port=10037)
print('successufully extract data')
result_lst = []

for line in task_lst:
    match_id = line['match_id']
    user_info_lst = user_info_at_localhost(match_id=match_id)
    dic_lst_to_file(lst_name=user_info_lst,
                    file_name='D:/python_code/crawler_opgg/crawler_result/test_1')

            



