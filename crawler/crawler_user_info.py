# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 21:50:59 2018

@author: fangyucheng
"""

from crawler_opgg.utils.retry_get_url import retry_get_url


def process_one_line(page_cate, process_dic):
    user_info = {}
    user_info[page_cate+'_headshot_kills_sum'] = process_dic['stats']['headshot_kills_sum']
    user_info[page_cate+'_kills_sum'] = process_dic['stats']['kills_sum']
    user_info[page_cate+'_damage_per_match'] = process_dic['stats']['damage_dealt_avg']
    user_info[page_cate+'_kills_max'] = process_dic['stats']['kills_max']
    user_info[page_cate+'_play_times'] = process_dic['stats']['matches_cnt']
    user_info[page_cate+'_chicken'] = process_dic['stats']['win_matches_cnt']
    user_info[page_cate+'_survived_second'] = process_dic['stats']['time_survived_avg']
    user_info[page_cate+'_deaths_num'] = process_dic['stats']['deaths_sum']
    user_info[page_cate+'_rating'] = process_dic['stats']['rating']
    return user_info


def user_info(user_id,
              season='2018-09',
              server='pc-as',
              mode='tpp'):
    """
    focus on tpp mode, may
    """
    solo_page = ('https://pubg.op.gg/api/users/' + user_id + 
                 '/ranked-stats?season=' + season + 
                 '&server=' + server + '&queue_size=1&mode=' + mode)
    double_page = ('https://pubg.op.gg/api/users/' + user_id + 
                   '/ranked-stats?season=' + season + 
                   '&server=' + server + '&queue_size=2&mode=' + mode)
    square_page = ('https://pubg.op.gg/api/users/' + user_id + 
                   '/ranked-stats?season=' + season + 
                   '&server=' + server + '&queue_size=4&mode=' + mode)
    get_page = retry_get_url(solo_page)
    page_dic = get_page.json()
    if len(page_dic) > 3:
        solo_dic = process_one_line(page_cate='solo', process_dic=page_dic)
    else:
        print("can't not get user_info solo page")
        solo_dic = {}
    get_page = retry_get_url(double_page)
    page_dic = get_page.json()
    if len(page_dic) > 3:
        double_dic = process_one_line(page_cate='double', process_dic=page_dic)
    else:
        print("can't not get user_info solo page")
        double_dic = {}
    solo_double_dic = dict(solo_dic, **double_dic)
    get_page = retry_get_url(square_page)
    page_dic = get_page.json()
    if len(page_dic) > 3:
        square_dic = process_one_line(page_cate='square', process_dic=page_dic)
    else:
        print("can't not get user_info solo page")
        square_dic = {}
    user_info_dic = dict(solo_double_dic, **square_dic)
    return user_info_dic
