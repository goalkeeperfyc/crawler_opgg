# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 14:19:00 2018

@author: fangyucheng
"""

import requests
import time
import asyncio
import re
import datetime
import json
import aiohttp
from bs4 import BeautifulSoup
##from crawler_sys.framework.video_fields_std import Std_fields_video
#from crawler_sys.utils.output_results import retry_get_url
from crawler.crawler_sys.utils.output_results import output_result
#from crawler_sys.utils.output_log import output_log
from crawler.crawler_sys.utils.trans_str_play_count_to_int import trans_play_count


"""
'电影': 'http://v.qq.com/x/list/movie',
'电视剧': 'http://v.qq.com/x/list/tv',
'综艺': 'http://v.qq.com/x/list/variety',
'动漫': 'http://v.qq.com/x/list/cartoon',
'少儿': 'http://v.qq.com/x/list/children',
'纪录片': 'http://v.qq.com/x/list/doco',
'微电影': 'http://v.qq.com/x/list/dv',
"""

lst_page_url_dic = {'音乐': 'http://v.qq.com/x/list/music',
                    '新闻': 'http://v.qq.com/x/list/news',
                    '军事': 'http://v.qq.com/x/list/military',
                    '娱乐': 'http://v.qq.com/x/list/ent',
                    '体育': 'http://v.qq.com/x/list/sports',
                    '游戏': 'http://v.qq.com/x/list/games',
                    '搞笑': 'http://v.qq.com/x/list/fun',
                    '王者荣耀': 'http://v.qq.com/x/list/kings',
                    '时尚': 'http://v.qq.com/x/list/fashion',
                    '生活': 'http://v.qq.com/x/list/life',
                    '母婴': 'http://v.qq.com/x/list/baby',
                    '汽车': 'http://v.qq.com/x/list/auto',
                    '科技': 'http://v.qq.com/x/list/tech',
                    '教育': 'http://v.qq.com/x/list/education',
                    '财经': 'http://v.qq.com/x/list/finance',
                    '房产': 'http://v.qq.com/x/list/house',
                    '旅游': 'http://v.qq.com/x/list/travel'}


def dic_lst_to_file(listname, filename):
    file = open(filename, 'a')
    for line in listname:
        json_line = json.dumps(line)
        file.write(json_line)
        file.write('\n')
    file.flush()
    file.close()


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
        task_url_lst_new = [value+'/?sort=5&offset='+ str(num) for num in num_lst]
        lst_page_task_lst.extend(task_url_lst_new)
        task_url_lst_hot = [value + '/?sort=40&offset=' + str(num) for num in num_lst]
        lst_page_task_lst.extend(task_url_lst_hot)
        task_url_lst_praise = [value+'/?sort=48&offset='+ str(num) for num in num_lst]
        lst_page_task_lst.extend(task_url_lst_praise)
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


async def asynchronous_get_lst_page(session, url):
    get_page = await session.get(url)
    page = await get_page.text("utf-8", errors="ignore")
    return page

async def asynchronous_get_video_page(session, data_dic):
    url = data_dic['url']
    play_count = data_dic['play_count']
    get_page = await session.get(url)
    page = await get_page.text("utf-8", errors="ignore")
    return {'page': page, 'play_count': play_count, 'url': url}


#async def lst_page777(loop,
#                      task_lst,
#                      ):
#    lst_result_lst = []
#    agg_video_data_lst = []
#    final_result_lst = []
#    lst_page_task_lst = lst_page_task(target_channel='游戏')
#    async with aiohttp.ClientSession() as sess_lst_page:
#        tasks = [loop.create_task(asynchronous_get_lst_page(sess_lst_page, url)) for url in lst_page_task_lst]
#        lst_result, unfinished = await asyncio.wait(tasks)
#        lst_result_lst = [l.result() for l in lst_result]
#        print("the length of lst_result_lst is %s" % len(lst_result_lst))
#    for lst_page in lst_result_lst:
#        video_data_lst = process_lst_page(resp=lst_page)
#        async with aiohttp.ClientSession() as sess_video_page:
#            task_video_page = [loop.create_task(asynchronous_get_video_page(sess_video_page, data_dic)) for data_dic in video_data_lst]
#            video_result, unfinished = await asyncio.wait(task_video_page)
#            video_page_download_result_lst = [v.result() for v in video_result]
#            for video_html in video_page_download_result_lst:
#                video_data_dic = process_video_page(resp_dic=video_html)
#                final_result_lst.append(video_data_dic)
#                print("the length of video list is %s" % len(agg_video_data_lst))
#            output_result()
#    return final_result_lst

def retry_get_lst_page(lsturl, 
                       retries_time=3):
    count = 0
    video_url_lst = []
    while count < retries_time:
        get_page = requests.get(lsturl)
        page = get_page.text
        video_url_lst = process_lst_page(resp=page)
        count += 1
        if video_url_lst != []:
            continue
    return video_url_lst


async def lst_page888(loop,
                      task_lst,
                      platform='腾讯视频',
                      output_to_file=True,
                      filepath='/home/fangyucheng/python_code',
                      output_to_es_raw=False,
                      es_index=None,
                      doc_type=None):
    final_result_lst = []
    for lsturl in task_lst:
        print("current lsturl is %s" % lsturl)
        video_url_lst = retry_get_lst_page(lsturl)
        if video_url_lst == []:
            continue
        print("get %s page url list whose length is %s" % (lsturl, len(video_url_lst)))
        async with aiohttp.ClientSession() as sess_video_page:
            task_video_page = [loop.create_task(asynchronous_get_video_page(sess_video_page, data_dic)) for data_dic in video_url_lst]
            video_result, unfinished = await asyncio.wait(task_video_page)
            video_page_download_result_lst = [v.result() for v in video_result]
            for video_html in video_page_download_result_lst:
                video_data_dic = process_video_page(resp_dic=video_html)
                print(video_data_dic)
                final_result_lst.append(video_data_dic)
                print("the length of video list is %s" % len(final_result_lst))
                if len(final_result_lst) >= 100:
                    output_result(result_Lst=final_result_lst,
                                  platform=platform,
                                  output_to_file=output_to_file,
                                  filepath=filepath,
                                  output_to_es_raw=output_to_es_raw,
                                  es_index=es_index,
                                  doc_type=doc_type)
                    final_result_lst.clear()
    if final_result_lst != []:
        output_result(result_Lst=final_result_lst,
                      platform=platform,
                      output_to_file=output_to_file,
                      filepath=filepath,
                      output_to_es_raw=output_to_es_raw,
                      es_index=es_index,
                      doc_type=doc_type)
    return final_result_lst


def process_video_page(resp_dic):
    url = resp_dic['url']
    play_count = resp_dic['play_count']
    page = resp_dic['page']
    soup = BeautifulSoup(page, 'html.parser')
    try:
        title = soup.find('h1',{'class': 'video_title _video_title'}).text
        title = title.replace('\n', '')
        title = title.replace('\t', '')
        # remove leading and trailing spaces
        title = re.sub('(^\s+)|(\s+$)', '', title)
    except:
        try:
            title = soup.find('h1', {'class': 'video_title'}).text
            title = title.replace('\n', '')
            title = title.replace('\t', '')
            title = re.sub('(^\s+)|(\s+$)', '', title)
        except:
            title = None
    try:
        releaser = soup.find('span', {'class': 'user_name'}).text
    except:
        releaser = None
        releaserUrl = None
    else:
        try:
            releaserUrl = soup.find('a', {'class': 'user_info'})['href']
        except:
            releaserUrl = None
    try:
        video_intro = soup.find('meta', {'itemprop': 'description'})['content']
    except:
        video_intro = None
    soup_find = soup.find("script", {"r-notemplate": "true"})
    if soup_find != None:
        midstep = soup_find.text
    else:
        print('Failed to get correct html text with soup')
        return None
    video_info_var_Lst = re.findall('var\s+VIDEO_INFO\s+=\s*{.+}', midstep)
    if video_info_var_Lst != []:
        video_info_var = video_info_var_Lst[0]
        video_info_json = re.sub('var\s+VIDEO_INFO\s+=\s*', '', video_info_var)
        try:
            video_info_dict = json.loads(video_info_json)
        except:
            print('Failed to transfer video_info_json to dict')
            video_info_dict = {}
        if video_info_dict != {}:
            if 'duration' in video_info_dict:
                duration_str = video_info_dict['duration']
                duration = int(duration_str)
            else:
                duration = None
            if 'title' in video_info_dict:
                title = video_info_dict['title']
            if 'video_checkup_time' in video_info_dict:
                release_time_str = video_info_dict['video_checkup_time']
                try:
                    release_time_ts = int(datetime.datetime.strptime(
                                        release_time_str, '%Y-%m-%d %H:%M:%S'
                                        ).timestamp()*1e3)
                except:
                    release_time_ts = None
            else:
                release_time_ts = None
    else:
        try:
            release_time_str = soup.find('span', {'class': 'tag_item'}).text
            re_lst = re.findall('\d+',release_time_str)
            release_time_raw = re_lst[0] + '-' + re_lst[1] + '-' + re_lst[2]
            release_time_ts = int(datetime.datetime.strptime(release_time_raw, '%Y-%m-%d').timestamp()*1e3)
        except:
            release_time_ts = None
        try:
            duration_str = re.findall('duration.*', page)[0]
            duration = int(re.findall('\d+', duration_str)[0])
        except:
            duration = None
    fetch_time = int(datetime.datetime.timestamp(datetime.datetime.now())*1e3)
    video_dict = {}
    video_dict['url'] = url
    video_dict['title'] = title
    video_dict['releaser'] = releaser
    video_dict['play_count'] = play_count
    video_dict['release_time'] = release_time_ts
    video_dict['duration'] = duration
    video_dict['fetch_time'] = fetch_time
    if releaserUrl is not None:
        video_dict['releaserUrl'] = releaserUrl
    if video_intro is not None:
        video_dict['video_intro'] = video_intro
    return video_dict


async def lst_page2(lsturl, **kwarg):
    result_lst = []
    get_page = requests.get(lsturl)
    resp = get_page.text
    video_lst = []
    video_lst = process_lst_page(resp)
    print("the length of video_lst is %s" % str(len(video_lst)))
    if video_lst != []:
        for video_dic in video_lst:
            try:
                play_count = video_dic['play_count']
            except:
                play_count = 0
            url = video_dic['url']
            async with aiohttp.ClientSession() as sess_video_page:
                get_video_page = await sess_video_page.get(url)
                video_page = await get_video_page.text()
                data_dic = process_video_page(resp=video_page)
                data_dic['play_count'] = play_count
                data_dic['url'] = url
                print(data_dic)
                result_lst.extend(data_dic)
    dic_lst_to_file(listname=result_lst,
                    filename='/home/fangyucheng/python_code/output_result7')
    return result_lst



start = time.time()
task_lst = lst_page_task()
#lst_page_task_lst = lst_page_task(target_channel='游戏')
#lst_page_task_lst2 = lst_page_task(target_channel='时尚')
#task_lst.extend(lst_page_task_lst)
#task_lst = task_lst[:34]
#task_lst.extend(lst_page_task_lst2)
#tasks = [asyncio.ensure_future(lst_page2(lsturl=url)) for url in task_lst]
loop = asyncio.get_event_loop()
loop.run_until_complete(lst_page888(loop, task_lst=task_lst))
cost_time = time.time() - start
print("the total cost of time is %s" % str(cost_time))