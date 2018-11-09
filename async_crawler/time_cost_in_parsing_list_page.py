# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 11:47:27 2018

@author: fangyucheng
"""

import requests
import time
from bs4 import BeautifulSoup
##from crawler_sys.framework.video_fields_std import Std_fields_video
#from crawler_sys.utils.output_results import retry_get_url
#from crawler_sys.utils.output_results import output_result
#from crawler_sys.utils.output_log import output_log
from crawler.crawler_sys.utils.trans_str_play_count_to_int import trans_play_count


lst_page_url_dic = {'电影': 'http://v.qq.com/x/list/movie',
                    '电视剧': 'http://v.qq.com/x/list/tv',
                    '综艺': 'http://v.qq.com/x/list/variety',
                    '动漫': 'http://v.qq.com/x/list/cartoon',
                    '少儿': 'http://v.qq.com/x/list/children',
                    '音乐': 'http://v.qq.com/x/list/music',
                    '纪录片': 'http://v.qq.com/x/list/doco',
                    '新闻': 'http://v.qq.com/x/list/news',
                    '军事': 'http://v.qq.com/x/list/military',
                    '娱乐': 'http://v.qq.com/x/list/ent',
                    '体育': 'http://v.qq.com/x/list/sports',
                    '游戏': 'http://v.qq.com/x/list/games',
                    '搞笑': 'http://v.qq.com/x/list/fun',
                    '微电影': 'http://v.qq.com/x/list/dv',
                    '时尚': 'http://v.qq.com/x/list/fashion',
                    '生活': 'http://v.qq.com/x/list/life',
                    '母婴': 'http://v.qq.com/x/list/baby',
                    '汽车': 'http://v.qq.com/x/list/auto',
                    '科技': 'http://v.qq.com/x/list/tech',
                    '教育': 'http://v.qq.com/x/list/education',
                    '财经': 'http://v.qq.com/x/list/finance',
                    '房产': 'http://v.qq.com/x/list/house',
                    '旅游': 'http://v.qq.com/x/list/travel'}


def lst_page_task(target_channel=None,
                  page_num_max=34,
                  lst_page_url_dic=lst_page_url_dic):
    if target_channel is not None:
        target_url = lst_page_url_dic[target_channel]
        lst_page_url_dic = {target_channel: target_url}
    lst_page_task_lst = []
    videos_in_one_page = 30
    num_lst = []
    for i in range(0, page_num_max):
        num = i * videos_in_one_page
        num_lst.append(num)
    for key, value in lst_page_url_dic.items():
        task_url_lst1 = [value + '/?sort=40&offset=' + str(num) for num in num_lst]
        lst_page_task_lst.extend(task_url_lst1)
        task_url_lst2 = [value+'/?sort=5&offset='+ str(num) for num in num_lst]
        lst_page_task_lst.extend(task_url_lst2)
    return lst_page_task_lst


def process_lst_page(resp):
    video_lst = []
    soup = BeautifulSoup(resp, 'html.parser')
    midstep = soup.find_all('li', {'class':'list_item'})
    for line in midstep:
        video_dic = {}
        url = line.a['href']
        find_play_count = BeautifulSoup(list(line)[-2], 'html.parser')
        play_count_str = find_play_count.find('span', {'class':'num'}).text.replace(' ', '')
        try:
            play_count = trans_play_count(play_count_str)
        except:
            play_count = 0
        video_dic = {'url': url,
                     'play_count': play_count}
        video_lst.append(video_dic)
    return video_lst


start = time.time()
task_lst = lst_page_task(target_channel='游戏')
result_lst = []
for line in task_lst:
    get_page = requests.get(line)
    page = get_page.text
    video_lst = process_lst_page(resp=page)
    result_lst.extend(video_lst)
    print("the length of result list is %s" % len(result_lst))
cost_time = time.time() - start
print("the total cost of time is %s" % str(cost_time))
