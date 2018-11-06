# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 14:19:00 2018

@author: fangyucheng
"""


import asyncio
import copy
import requests
import re
import sys
import datetime
import json
import aiohttp
from bs4 import BeautifulSoup
from crawler_sys.framework.video_fields_std import Std_fields_video
from crawler_sys.utils.output_results import retry_get_url
from crawler_sys.utils.output_results import output_result
from crawler_sys.utils.output_log import output_log
from crawler_sys.utils.trans_str_play_count_to_int import trans_play_count


#    def __init__(self, timeout=None, platform='腾讯视频'):
#        if timeout==None:
#            self.timeout = 10
#        else:
#            self.timeout = timeout
#        self.platform = platform
#        std_fields = Std_fields_video()
#        self.video_data = std_fields.video_data
#        self.video_data['platform'] = self.platform
#        # remove fields that crawled data don't have
#        pop_key_Lst = ['describe', 'repost_count', 'isOriginal',
#                       'video_id']
#        for popk in pop_key_Lst:
#            self.video_data.pop(popk)

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
#        self.legal_list_page_urls = []
#        self.legal_channels = []
#        for ch in self.list_page_url_dict:
#            list_page_url = self.list_page_url_dict[ch]
#            self.legal_list_page_urls.append(list_page_url)
#            self.legal_channels.append(ch)
    
def lst_page_task(self, page_num_max=34,
                  lst_page_url_dic=lst_page_url_dic):
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

async def request(self, url, **kwarg):
    async with aiohttp.ClientSession() as session:
        get_page = await session.get(url, **kwarg)
        page = await get_page.text()
    return page

async def lst_page(self, listurl)
    
    
    
    
    def process_video_page_response(self, response):
        if response is None:
            return None
        else:
            response.encoding = 'utf-8'
            page = response.text
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
                    if 'view_all_count' in video_info_dict:
                        play_count = video_info_dict['view_all_count']
                        data_source = 'video_info'
                    else:
                        try:
                            play_count_str = re.findall('interactionCount.*', page)[0]
                            play_count = re.findall('\d+', play_count_str)[0]
                            play_count = int(play_count)
                            data_source = 'interactioncount'
                        except:
                            play_count = None
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
                    play_count_str = re.findall('interactionCount.*', page)[0]
                    play_count = re.findall('\d+', play_count_str)[0]
                    play_count = int(play_count)
                    data_source = 'interactioncount'
                except:
                    play_count = None
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
            video_dict = copy.deepcopy(self.video_data)
            if play_count != None:
                video_dict['title'] = title
                video_dict['data_source'] = data_source
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



    def video_page(self, url, channel=None):
        if 'm.v.qq.com' in url:
            vid_str = ' '.join(re.findall('o/d/y/.*.html', url))
            vid = vid_str.replace('o/d/y/', '').replace('.html', '')
            url = 'https://v.qq.com/x/page/' + vid + '.html'
        get_page = retry_get_url(url, timeout=self.timeout)
        if get_page is None:
            return None
        else:
            get_page.encoding = 'utf-8'
            page = get_page.text
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
            if video_info_var_Lst!=[]:
                video_info_var = video_info_var_Lst[0]
                video_info_json = re.sub('var\s+VIDEO_INFO\s+=\s*', '', video_info_var)
                try:
                    video_info_dict = json.loads(video_info_json)
                except:
                    print('Failed to transfer video_info_json to dict '
                          'for url: ' % url)
                    video_info_dict = {}
                if video_info_dict != {}:
                    if 'duration' in video_info_dict:
                        duration_str = video_info_dict['duration']
                        duration = int(duration_str)
                    else:
                        duration = None
                    if 'title' in video_info_dict:
                        title = video_info_dict['title']
                    if 'view_all_count' in video_info_dict:
                        play_count = video_info_dict['view_all_count']
                        data_source = 'video_info'
                    else:
                        try:
                            play_count_str = re.findall('interactionCount.*', page)[0]
                            play_count = re.findall('\d+', play_count_str)[0]
                            play_count = int(play_count)
                            data_source = 'interactioncount'
                        except:
                            play_count = None
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
                    play_count_str = re.findall('interactionCount.*', page)[0]
                    play_count = re.findall('\d+', play_count_str)[0]
                    play_count = int(play_count)
                    data_source = 'interactioncount'
                except:
                    play_count = None
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
            video_dict = copy.deepcopy(self.video_data)
            if play_count != None:
                video_dict['title'] = title
                video_dict['data_source'] = data_source
                if channel is not None:
                    video_dict['channel'] = channel
                video_dict['releaser'] = releaser
                video_dict['play_count'] = play_count
                video_dict['release_time'] = release_time_ts
                video_dict['duration'] = duration
                video_dict['url'] = url
                video_dict['fetch_time'] = fetch_time
                if releaserUrl is not None:
                    video_dict['releaserUrl'] = releaserUrl
                if video_intro is not None:
                    video_dict['video_intro'] = video_intro
            return video_dict


    async def list_page(self, listurl,
                        channel=None,
                        output_to_file=False,
                        filepath=None,
                        output_to_es_raw=False,
                        output_to_es_register=False,
                        push_to_redis=False,
                        page_num_max=34,
                        output_es_index=None,
                        output_doc_type=None,
                        ):
        if channel is None:
            channel = listurl.split('list/')[-1]
        #listurl=http://v.qq.com/x/list/fashion/
        list_data_Lst = []

        #最近热播
        listpage = 
        #最近上架
        for listurls in listpage:
            get_page = retry_get_url(listurls, timeout=self.timeout)
            if get_page is None:
                print('Failed to get page for list page url: %s'
                      % listurls)
                return None
            get_page.encoding = 'utf-8'
            page = get_page.text
            print(listurls)
            soup = BeautifulSoup(page, 'html.parser')
            midstep = soup.find_all('li', {'class':'list_item'})
            for line in midstep:
                one_video_dic = {}
                url = line.a['href']
                try:
                    one_video_dic = self.video_page(url, channel)
                except:
                    print('failed to get data from %s' % url)
                else:
                    find_play_count = BeautifulSoup(list(line)[-2], 'html.parser')
                    play_count_str = find_play_count.find('span', {'class':'num'}).text.replace(' ', '')
                    try:
                        play_count = trans_play_count(play_count_str)
                    except:
                        play_count = 0
                    one_video_dic['play_count'] = play_count
                    list_data_Lst.append(one_video_dic)

                if len(list_data_Lst) >= 100:
                    if output_es_index != None and output_doc_type != None:
                        output_result(list_data_Lst,
                                      self.platform,
                                      output_to_file=output_to_file,
                                      filepath=filepath,
                                      output_to_es_raw=output_to_es_raw,
                                      output_to_es_register=output_to_es_register,
                                      push_to_redis=push_to_redis,
                                      es_index=output_es_index,
                                      doc_type=output_doc_type)
                        list_data_Lst.clear()
                    else:
                        output_result(list_data_Lst,
                                      self.platform,
                                      output_to_file=output_to_file,
                                      filepath=filepath,
                                      output_to_es_raw=output_to_es_raw,
                                      output_to_es_register=output_to_es_register,
                                      push_to_redis=push_to_redis)
                        list_data_Lst.clear()

        if list_data_Lst != []:
            if output_es_index != None and output_doc_type != None:
                output_result(list_data_Lst,
                              self.platform,
                              output_to_file=output_to_file,
                              filepath=filepath,
                              output_to_es_raw=output_to_es_raw,
                              output_to_es_register=output_to_es_register,
                              push_to_redis=push_to_redis,
                              es_index=output_es_index,
                              doc_type=output_doc_type)
                list_data_Lst.clear()
            else:
                output_result(list_data_Lst,
                              self.platform,
                              output_to_file=output_to_file,
                              filepath=filepath,
                              output_to_es_raw=output_to_es_raw,
                              output_to_es_register=output_to_es_register,
                              push_to_redis=push_to_redis)
                list_data_Lst.clear()
        return list_data_Lst





lst_page_task_lst = lst_page_task()
    
tasks = [asyncio.ensure_future(request()) for _ in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
releaserUrl = 'http://v.qq.com/vplus/aa39c0733cf737d428019ebd7c7bd47c/videos'
video_page2 = test.releaser_page(releaserUrl,
                                 releaser_page_num_max=2000,
                                 output_to_es_raw=True,
                                 output_es_index='test2',
                                 output_doc_type='fyc1102')