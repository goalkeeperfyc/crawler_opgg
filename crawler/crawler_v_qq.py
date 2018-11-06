# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 14:19:00 2018

independent function:
1 list page
2 search page
3 video page
4 releaser page

All function take parameters and return dict list.

parameters:
1 list page: url
2 search page: keyword
3 video page: url
4 releaser page: url


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


class Crawler_v_qq():

    def __init__(self, timeout=None, platform='腾讯视频'):
        if timeout==None:
            self.timeout = 10
        else:
            self.timeout = timeout
        self.platform = platform
        std_fields = Std_fields_video()
        self.video_data = std_fields.video_data
        self.video_data['platform'] = self.platform
        # remove fields that crawled data don't have
        pop_key_Lst = ['describe', 'repost_count', 'isOriginal',
                       'video_id']
        for popk in pop_key_Lst:
            self.video_data.pop(popk)

        self.list_page_url_dict = {
            '电影': 'http://v.qq.com/x/list/movie',
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
            '旅游': 'http://v.qq.com/x/list/travel',
            }
        self.legal_list_page_urls = []
        self.legal_channels = []
        for ch in self.list_page_url_dict:
            list_page_url = self.list_page_url_dict[ch]
            self.legal_list_page_urls.append(list_page_url)
            self.legal_channels.append(ch)

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


    def search_page(self, keyword):
        search_page_Lst=[]
        def process_one_line(data_line):
            url=data_line.h2.a['href']
            dicdicdic=self.video_page(url)
            return dicdicdic
        search_url = ['https://v.qq.com/x/search?q='+keyword+'&cur={}'.format(str(i)) for i in range(1,6)]
        for urls in search_url:
            get_page=requests.get(urls, timeout=self.timeout)
            print(urls)
            get_page.encoding='utf-8'
            page=get_page.text
            soup = BeautifulSoup(page,'html.parser')
            tencent = soup.find_all("div", { "class" : "result_item result_item_h _quickopen" })
            for data_line in tencent:
                one_line_dic=process_one_line(data_line)
                print('get one line done')
                search_page_Lst.append(one_line_dic)
        return search_page_Lst


    def list_page(self, listurl, channel=None,
                  output_to_file=False, filepath=None,
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
        listnum = []
        videos_in_one_page = 30
        for i in range(0, page_num_max):
            list_num = i * videos_in_one_page
            listnum.append(list_num)
        #最近热播
        listpage = [listurl + '/?sort=40&offset={}'.format(str(i)) for i in listnum]
        #最近上架
        #listpage=[listurl+'?sort=5&offset={}'.format(str(i)) for i in listnum]
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
                    find_play_count = BeautifulSoup(list(line)[-2], 'html.parser')
                    play_count_str1 = find_play_count.find('span', {'class':'num'}).text
                    play_count_str2 = play_count_str1.replace(' ', '')
                    try:
                        play_count = trans_play_count(play_count_str2)
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
                except:
                    print('failed to get data from %s' % url)
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


    def doc_list_page(self, listurl):
        #listurl=http://v.qq.com/x/list/fashion/
        done=open('done_qq','a')
        result=open('result_qq','a')
        error=open('error_qq','a')
        list_data_Lst=[]
        listnum=[]
        for i in range(0,93):
            list_num=i*30
            listnum.append(list_num)
        #最近热播
        listpage=[listurl+'?&offset={}'.format(str(i)) for i in listnum]
        #最近上架
        #listpage=[listurl+'?sort=5&offset={}'.format(str(i)) for i in listnum]
        for listurl in listpage:
            get_page=requests.get(listurl, timeout=self.timeout)
            get_page.encoding='utf-8'
            page = get_page.text
            print(listurl)
            done.write(listurl)
            done.write('\n')
            done.flush()
            soup = BeautifulSoup(page,'html.parser')
            midstep=soup.find_all('strong',{'class':'figure_title'})
            for line in midstep:
                album_name=line.text
                url=line.a['href']
                get_page=requests.get(url, timeout=self.timeout)
                get_page.encoding='utf-8'
                page = get_page.text
                soup = BeautifulSoup(page,'html.parser')
                try:
                    get_all_url=soup.find('ul',{'class':'figure_list _hot_wrapper'})
                    url_agg=get_all_url.find_all('a',{'class':'figure_detail'})
                    urllist=[]
                    for line in url_agg:
                        url_part=line['href']
                        url='https://v.qq.com'+url_part
                        urllist.append(url)
                    for url in urllist:
                        try:
                            one_video=self.video_page(url)
                            one_video['album_name']=album_name
                            print(url)
                            list_data_Lst.append(one_video)
                            one_video_json=json.dumps(one_video)
                            result.write(one_video_json)
                            result.write('\n')
                            result.flush()
                        except AttributeError:
                            D0={'url':url,'album_name':album_name}
                            print('there is an error')
                            json_D0=json.dumps(D0)
                            error.write(json_D0)
                            error.write('\n')
                            error.flush()
                except:
                   one_video=self.video_page(url)
                   one_video['album_name']=album_name
                   print(url)
                   list_data_Lst.append(one_video)
                   one_video_json=json.dumps(one_video)
                   result.write(one_video_json)
                   result.write('\n')
                   result.flush()
        done.close()
        result.close()
        error.close()
        return list_data_Lst


    def doc_list_reborn(self, listurl, x):
        #listurl=http://v.qq.com/x/list/fashion/
        done=open('done_qq','a')
        result=open('result_qq','a')
        error=open('error_qq','a')
        list_data_Lst=[]
        listnum=[]
        for i in range(x,93):
            list_num=i*30
            listnum.append(list_num)
        #最近热播
        listpage=[listurl+'?sort=40&offset={}'.format(str(i)) for i in listnum]
        #最近上架
        #listpage=[listurl+'?sort=5&offset={}'.format(str(i)) for i in listnum]
        for listurl in listpage:
            get_page=requests.get(listurl, timeout=self.timeout)
            get_page.encoding='utf-8'
            page = get_page.text
            print(listurl)
            done.write(listurl)
            done.write('\n')
            done.flush()
            soup = BeautifulSoup(page,'html.parser')
            midstep=soup.find_all('strong',{'class':'figure_title'})
            for line in midstep:
                album_name=line.text
                url=line.a['href']
                get_page=requests.get(url, timeout=self.timeout)
                get_page.encoding='utf-8'
                page = get_page.text
                soup = BeautifulSoup(page,'html.parser')
                try:
                    get_all_url=soup.find('ul',{'class':'figure_list _hot_wrapper'})
                    url_agg=get_all_url.find_all('a',{'class':'figure_detail'})
                    urllist=[]
                    for line in url_agg:
                        url_part=line['href']
                        url='https://v.qq.com'+url_part
                        urllist.append(url)
                    for url in urllist:
                        try:
                            one_video=self.video_page(url)
                            one_video['album_name']=album_name
                            print(url)
                            list_data_Lst.append(one_video)
                            one_video_json=json.dumps(one_video)
                            result.write(one_video_json)
                            result.write('\n')
                            result.flush()
                        except:
                            D0={'url':url,'album_name':album_name}
                            print('there is an error')
                            json_D0=json.dumps(D0)
                            error.write(json_D0)
                            error.write('\n')
                            error.flush()
                except:
                    try:
                        one_video=self.video_page(url)
                        one_video['album_name']=album_name
                        print(url)
                        list_data_Lst.append(one_video)
                        one_video_json=json.dumps(one_video)
                        result.write(one_video_json)
                        result.write('\n')
                        result.flush()
                    except:
                        D0={'url':url,'album_name':album_name}
                        print('there is an error')
                        json_D0=json.dumps(D0)
                        error.write(json_D0)
                        error.write('\n')
                        error.flush()
        done.close()
        result.close()
        error.close()
        return list_data_Lst


    def renew_playcount(self, taskname,resultname,no_resultname):
        task=open(taskname)
        result=open(resultname,'a')
        result_lst=[]
        no_result=open(no_resultname,'a')
        task_lst=[]
        for line in task:
            new_line=line.replace('null','None')
            line_dic=eval(new_line)
            task_lst.append(line_dic)
        for line in task_lst:
            url=line['url']
            if line['playcount']!=0:
                get_page=requests.get(url, timeout=self.timeout)
                get_page.encoding='utf-8'
                page = get_page.text
                soup = BeautifulSoup(page,'html.parser')
                try:
                    midstep = soup.find("script",{"r-notemplate":"true"}).text
                    playcount = re.findall(r'"view_all_count":[0-9]{1,10}',
                                    ','.join(re.findall(r'VIDEO_INFO.*"view_all_count":[0-9]{1,10}',
                                                        midstep)))[0].split(':')[1]
                except:
                    print('Catched exception, didn\'t find view_all_count in var VIDEO_INFO')
                    playcount=line['playcount']
                    no_result.write(url)
                    no_result.write('\n')
                    no_result.flush()
                fetch_time=int(datetime.datetime.timestamp(datetime.datetime.now())*1e3)
                line['playcount']=playcount
                line['fetch_time']=fetch_time
                print(url)
                #del line_dic['playcount']
                result_lst.append(line)
                json_line=json.dumps(line)
                result.write(json_line)
                result.write('\n')
                result.flush()
            else:
                no_result.write(url)
                no_result.write('\n')
                no_result.flush()
                print('no play_count')
        task.close()
        result.close()
        no_result.close()
        return result_lst


    def restart(self,total_url,donename):
        totalurl=open(total_url)
        total_lst=[]
        for line in totalurl:
            url=line.replace('\n','')
            total_lst.append(url)
        pre_done=open(donename)
        pre_done_lst=[]
        for line in pre_done:
            url=line.replace('\n','')
            pre_done_lst.append(url)
        url_lst=[]
        for url in total_lst:
            if url not in pre_done_lst:
                url_lst.append(url)
        return url_lst

    def error_url(self, url,error_file):
        if error_file==sys.stdout:
            print(url)
        else:
            error = open(error_file,'a')
            error.write(url)
            error.write('\n')
            error.flush()


    def get_releaser_id(self,releaserUrl):
        get_page=requests.get(releaserUrl, timeout=self.timeout)
        get_page.encoding='utf-8'
        page=get_page.text
        soup = BeautifulSoup(page,'html.parser')
        releaser_id=soup.find('span',{'class':'sns_btn'}).a['data-vuin']
        releaser = soup.find('span',{'class':'txt'}).text
        D0 = {'releaser':releaser,'releaser_id':releaser_id}
        return D0


    def get_release_time_from_str(self,rt_str):
        minute = '分钟'
        hour = '小时'
        day = '天'
        if minute in rt_str:
            rt_int = int(re.findall('\d+',rt_str)[0])
            rt = datetime.datetime.timestamp(datetime.datetime.now())-rt_int*60
            release_time = int(rt*1e3)
        elif hour in rt_str:
            rt_int = int(re.findall('\d+',rt_str)[0])
            rt = datetime.datetime.timestamp(datetime.datetime.now())-rt_int*3600
            release_time = int(rt*1e3)
        elif day in rt_str:
            rt_int = int(re.findall('\d+',rt_str)[0])
            rt = datetime.datetime.timestamp(datetime.datetime.now())-rt_int*3600*60
            release_time = int(rt*1e3)
        else:
            release_time = int(datetime.datetime.strptime(rt_str, '%Y-%m-%d').timestamp()*1e3)
        return release_time



    def releaser_page(self, releaserUrl,
                      output_to_file=False, filepath=None,
                      output_to_es_raw=False,
                      output_to_es_register=False,
                      push_to_redis=False,
                      releaser_page_num_max=30,
                      output_es_index=None,
                      output_doc_type=None):

        print('Processing releaserUrl %s' % releaserUrl)
        result_Lst = []
        releaser_info = self.get_releaser_id(releaserUrl)
        releaser_id = releaser_info['releaser_id']
        releaser = releaser_info['releaser']
        pagenum = 1
        if releaser_id != None:
            while pagenum <= releaser_page_num_max:
                releaser_page_url = ('http://c.v.qq.com/vchannelinfo?otype=json&uin='+releaser_id+'&qm=1&pagenum='
                                     + str(pagenum) + '&num=24&sorttype=0&orderflag=0')
                print('Page number: %d' % pagenum)
                print('result Lst len %d' % len(result_Lst))
                try:
                    get_page = retry_get_url(releaser_page_url,
                                             timeout=self.timeout)
                except:
                    get_page = None
                if get_page != None and get_page.status_code == 200:
                    get_page.encoding = 'utf-8'
                    page = get_page.text
                    real_page = page[13:-1]
                    real_page = real_page.replace('null', 'None')
                    try:
                        get_page_dic = eval(real_page)
                        page_dic = get_page_dic['videolst']
                    except:
                        page_dic = None
                    if pagenum == 1 and get_page_dic is not None:
                        total_video = get_page_dic['vtotal']
                        if total_video%24 == 0:
                            releaser_page_num_max_uncertain = int(total_video/24)
                        else:
                            releaser_page_num_max_uncertain = int(total_video/24)+1
                        if releaser_page_num_max > releaser_page_num_max_uncertain:
                            releaser_page_num_max = releaser_page_num_max_uncertain
                    if page_dic != None:
                        for a_video in page_dic:
                            try:
                                title = a_video['title']
                                play_count_str = a_video['play_count']
                                if '万' in play_count_str :
                                    play_count_str = play_count_str.replace('万', '')
                                    play_count = int(float(play_count_str)*1e4)
                                else:
                                    try:
                                        play_count = int(play_count_str)
                                    except:
                                        play_count_str = play_count_str.replace(',', '')
                                        play_count = int(play_count_str)
                                rt_str = a_video['uploadtime']
                                release_time = self.get_release_time_from_str(rt_str)
                                url = a_video['url']
                                duration_str = a_video['duration']
                                segs = duration_str.count(':')+1
                                seg_Lst = duration_str.split(':')
                                if segs == 2:
                                    s_hour = 0
                                    s_min = int(seg_Lst[0])
                                    s_sec = int(seg_Lst[1])
                                elif segs == 3:
                                    s_hour = int(seg_Lst[0])
                                    s_min = int(seg_Lst[1])
                                    s_sec = int(seg_Lst[2])
                                else:
                                    pass
                                duration = s_hour*3600 + s_min*60 + s_sec
                                fetch_time = int(datetime.datetime.timestamp(datetime.datetime.now())*1e3)
                                self.video_data['releaserUrl'] = releaserUrl
                                self.video_data['title'] = title
                                self.video_data['duration'] = duration
                                self.video_data['url'] = url
                                self.video_data['play_count'] = play_count
                                self.video_data['releaser'] = releaser
                                self.video_data['releaser_id_str'] = releaser_id
                                self.video_data['release_time'] = release_time
                                self.video_data['fetch_time'] = fetch_time
                                get_data = copy.deepcopy(self.video_data)
                                result_Lst.append(get_data)
                                if len(result_Lst) >= 100:
                                    if output_es_index != None and output_doc_type != None:
                                        output_result(result_Lst, self.platform,
                                                      output_to_file=output_to_file,
                                                      filepath=filepath,
                                                      output_to_es_raw=output_to_es_raw,
                                                      output_to_es_register=output_to_es_register,
                                                      push_to_redis=push_to_redis,
                                                      es_index=output_es_index,
                                                      doc_type=output_doc_type
                                                     )
                                        result_Lst.clear()
                                    else:
                                        output_result(result_Lst, self.platform,
                                                      output_to_file=output_to_file,
                                                      filepath=filepath,
                                                      output_to_es_raw=output_to_es_raw,
                                                      output_to_es_register=output_to_es_register,
                                                      push_to_redis=push_to_redis)
                                        result_Lst.clear()
                            except:
                                print(a_video)
                else:
                    pass
                pagenum += 1
        if result_Lst != []:
            if output_es_index != None and output_doc_type != None:
                output_result(result_Lst, self.platform,
                              output_to_file=output_to_file,
                              filepath=filepath,
                              output_to_es_raw=output_to_es_raw,
                              output_to_es_register=output_to_es_register,
                              push_to_redis=push_to_redis,
                              es_index=output_es_index,
                              doc_type=output_doc_type
                             )
            else:
                output_result(result_Lst, self.platform,
                              output_to_file=output_to_file,
                              filepath=filepath,
                              output_to_es_raw=output_to_es_raw,
                              output_to_es_register=output_to_es_register,
                              push_to_redis=push_to_redis)
        return result_Lst


    def get_releaser_follower_num(self, releaserUrl):
        get_page = requests.get(releaserUrl)
        get_page.encoding = 'utf-8'
        page = get_page.text
        soup = BeautifulSoup(page, 'html.parser')
        try:
            follower_str = soup.find('span', {'class': 'num j_rss_count'}).text
            follower_num = trans_play_count(follower_str)
            print('%s follower number is %s' % (releaserUrl, follower_num))
            return follower_num
        except:
            print("can't can followers")


# test
if __name__=='__main__':
    test = Crawler_v_qq()
    releaserUrl = 'http://v.qq.com/vplus/aa39c0733cf737d428019ebd7c7bd47c/videos'
    video_page2 = test.releaser_page(releaserUrl,
                                     releaser_page_num_max=2000,
                                     output_to_es_raw=True,
                                     output_es_index='test2',
                                     output_doc_type='fyc1102')