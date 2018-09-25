# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 10:30:31 2018

@author: fangyucheng
"""

import re
import requests
import pymysql
import datetime
from elasticsearch import Elasticsearch
from timeShiftAggregation import make_up_sql
#from crawler_sys.utils import Metaorphosis as meta



headers = {"host": "www.365yg.com",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "zh-CN,en-US;q=0.7,en;q=0.3",
           "Accept-Encoding": "gzip, deflate",
           "DNT": "1",
           "Connection": "keep-alive",
           "Upgrade-Insecure-Requests": "1"}


hosts = '192.168.17.11'
port = 80
user_id = 'fangyucheng'
password = 'VK0FkWf1fV8f'
http_auth = (user_id, password)
lose_re_url = []
es = Elasticsearch(hosts=hosts, port=port, http_auth=http_auth)


connection = pymysql.connect(host='localhost', user='root', passwd='goalkeeper@1',
                             db='add_target_releaser', port=3306,
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

connection_ip = pymysql.connect(host='localhost', user='root', passwd='goalkeeper@1',
                                db='proxy_pool', port=3306,
                                cursorclass=pymysql.cursors.DictCursor)
cursor_ip = connection_ip.cursor()

#one time is enough
#data_lst = meta.str_file_to_lst('D:/add_target_releaser/toutiao_rank10001_100000/cannot_find_releaerurl_by_es_dead2.txt')
#data_lst.remove(data_lst[0])
#
#
#for line in data_lst:
#    line_dic = {'platform': 'toutiao',
#                'test_or_not': 0,
#                'releaser': line}
#    write_into_sql = make_up_sql.make_up_replace_sql(table_name='target_releaser', 
#                                                     input_dic=line_dic)
#    cursor.execute(write_into_sql)
#connection.commit()

count = 0
change_ip = 1
remain = 1000
while remain >= 1:
    search_sql = "select * from target_releaser where test_or_not=0"
    remain = cursor.execute(search_sql)
    task_lst = cursor.fetchall()[0]
    releaser_info_id = task_lst['id']
    releaser = task_lst['releaser']
    platform = task_lst['platform']
    search_url = {
          "query": {
            "bool": {
              "filter": [{"term": {"releaser.keyword": releaser}},
                         {"term":{"platform.keyword": platform}}]}},
                  "size": 1}

    search_url_re = es.search(index='short-video-production',
                              doc_type='daily-url',
                              body=search_url,
                              request_timeout=100,
                              size=1)
    print("get %s's video from es" % releaser)
    try:
        video_url = search_url_re['hits']['hits'][0]['_source']['url']
    except:
        update_sql = "update target_releaser set test_or_not=99 where id='" + str(releaser_info_id) + "'"
        cursor.execute(update_sql)
        connection.commit()
        print('releaser %s video url does not exist')
        continue
    if change_ip == 1:
        print('change ip address')
        search_ip_sql = "select * from useful_ip where availability=1"
        cursor_ip.execute(search_ip_sql)
        whole_ip_info = cursor_ip.fetchall()[0]
        proxy_dic = {whole_ip_info['category']: whole_ip_info['whole_ip_address']}
        ip_id = whole_ip_info['id']
    print('new ip got %s' % proxy_dic)
    if "toutiao.com" in video_url:
        video_id_str = ' '.join(re.findall('/group/[0-9]+', video_url))
        video_id = ' '.join(re.findall('\d+', video_id_str))
        video_url = 'http://www.365yg.com/a' + video_id
    elif "365yg.com" in video_url:
        video_url = video_url
    else:
        update_sql = "update target_releaser set test_or_not=99 where id='" + str(releaser_info_id) + "'"
        cursor.execute(update_sql)
        connection.commit()
        print('releaser %s video url is strange')
        continue
    try:
        get_page = requests.get(url=video_url, headers=headers, proxies=proxy_dic, timeout=10)
        change_ip = 0
    except:
        update_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        update_ip_sql = "update useful_ip set availability=0 WHERE id =" + str(ip_id) 
        cursor_ip.execute(update_ip_sql)
        connection_ip.commit()
        change_ip = 1
        print('old ip address is bad')
        continue
    try:
        page = get_page.text
        get_releaser_id = ' '.join(re.findall('/c/user/[0-9]+/', page))
        if get_releaser_id != '':
            releaser_id = ' '.join(re.findall('\d+', get_releaser_id))
            releaserUrl = 'www.365yg.com/c/user/' + str(releaser_id)
            line_dic = {'releaser': releaser,
                        'releaserUrl': releaserUrl,
                        'url': video_url}
            update_sql = "update target_releaser set test_or_not=1 where id='" + str(releaser_info_id) + "'"
            cursor.execute(update_sql)
            update_sql = make_up_sql.make_up_replace_sql(table_name='video_info', input_dic=line_dic)
            cursor.execute(update_sql)
            connection.commit()
            print('find releaserUrl %s' % releaserUrl)
        else:
            update_sql = "update target_releaser set test_or_not=99 where id='" + str(releaser_info_id) + "'"
            cursor.execute(update_sql)
            connection.commit()
            print('releaser %s video page does not exist')
            continue
    except:
        pass



