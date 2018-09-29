# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 21:50:59 2018

@author: fangyucheng
"""

import datetime
from bs4 import BeautifulSoup
from crawler_opgg.utils.retry_get_url import retry_get_url
from crawler_opgg.utils.output_result import output_result


def get_season():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m')


def match_id(user_name,
             table_name='match_info'):
    result_lst = []
    season = get_season()
    user_home_page = 'https://pubg.op.gg/user/' + user_name + '?server=pc-as'
    get_page = retry_get_url(user_home_page)
    get_page.encoding = 'utf-8'
    page = get_page.text
    soup = BeautifulSoup(page, 'html.parser')
    match_lst = soup.find_all('li', {'data-selector': 'total-played-game-item'})
    for line in match_lst:
        match_id = line.find('div', {'class': 'matches-item__column matches-item__column--team'}).div['data-u-id']
        create_time = datetime.datetime.strftime(datetime.datetime.now(), 
                                                 '%Y-%m-%d %H:%M:%S')
        match_info = {'create_time': create_time,
                      'match_id': match_id,
                      'season': season,
                      'used': 0}
        result_lst.append(match_info)
        if len(result_lst) >= 100:
            output_result(result_lst=result_lst,
                          table_name=table_name)
            result_lst.clear()
    if len(result_lst) != []:
        output_result(result_lst,
                      table_name=table_name)
    return result_lst


def get_user_id(user_home_page):
    get_page = retry_get_url(user_home_page)
    get_page.encoding = 'utf-8'
    page = get_page.text
    soup = BeautifulSoup(page, 'html.parser')
    user_id = soup.find('div', {'id': 'userNickname'})['data-user_id']
    return user_id


def user_info(match_id,
              table_name='user_info',
              host='localhost'):
    result_lst = []
    url = 'https://pubg.op.gg/api/matches/' + match_id
    get_page = retry_get_url(url)
    page_dic = get_page.json()
    user_info_lst = page_dic['teams']
    for line in user_info_lst:
        user_lst = line['participants']
        for line in user_lst:
            user_name = line['user']['nickname']
            user_home_page = line['user']['profile_url']
            user_id = get_user_id(user_home_page)
            create_time = datetime.datetime.strftime(datetime.datetime.now(), 
                                                     '%Y-%m-%d %H:%M:%S')
            user_info_dic = {'user_name': user_name,
                             'user_id': user_id,
                             'create_time': create_time}
            print('got user_info %s' % user_name)
            result_lst.append(user_info_dic)

    if result_lst != []:
        output_result(result_lst,
                      table_name=table_name,
                      host=host)
    return result_lst


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


def user_performance(user_id,
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

