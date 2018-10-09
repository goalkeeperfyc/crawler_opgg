# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 10:11:24 2018

@author: fangyucheng
"""


from crawler_opgg.crawler.crawler_user_info import user_info
from crawler_opgg.crawler.crawler_user_info import user_performance
from crawler_opgg.utils.update_status_in_mysql import update_status


def get_info_and_update_status(match_info_dic):
    record_id = match_info_dic['id']
    update_sql = "update match_info set used=1 where id=" + str(record_id)
    update_status(update_sql)
    print('update success %s' % match_info_dic['match_id'])
    match_id = match_info_dic['match_id']
    user_info(match_id)


def get_performance_and_update_status(user_info_dic):
    """
    print is processing in function user_performance
    """
    record_id = user_info_dic['id']
    user_id = user_info_dic['user_id']
    user_performance(user_id)
    update_sql = "update user_info set used=1 where id=" + str(record_id)
    update_status(update_sql)