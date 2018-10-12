# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 14:11:54 2018

@author: fangyucheng
"""

from crawler_opgg.utils.extract_from_database import extract_data

search_sql = "select * from user_performance"

data_lst = extract_data(search_sql, host='cdb-1y1l8q6e.bj.tencentcdb.com',
                        port=10037)

for line in data_lst:
    try:
        line['headshot_per_4'] = line['square_headshot_kills_sum']/line['square_kills_sum']
    except:
        line['headshot_per_4'] = 0

big_brother = []
for line in data_lst:
    if line['headshot_per_4'] >= 0.3:
        big_brother.append(line)

super_big_brother = []
for line in data_lst:
    if line['headshot_per_4'] >= 0.4:
        super_big_brother.append(line)

no_data_lst = []
for line in data_lst:
    if line['solo_play_times'] == 0 and line['double_play_times'] == 0 and line['square_play_times'] == 0:
        no_data_lst.append(line)

