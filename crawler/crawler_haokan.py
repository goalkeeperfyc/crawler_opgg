# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 21:04:19 2018

@author: fangyucheng
"""


import copy
import requests
from crawler_sys.utils.output_results import output_result
from crawler_sys.framework.video_fields_std import Std_fields_video


def releaser_page(releaser_id,
                  page_num_max=30,
                  ):
    
    result_lst = []
    video_data = Std_fields_video().video_data
    page_num = 1
    releaserUrl = 'https://sv.baidu.com/haokan/api?log=vhk&tn=1015351w&ctn=1015351w&stn=&imei=008796749793280&cuid=0C14B366AD2664656A4CD5BAB3C48291|082397947697800&os=android&osbranch=a0&ua=720_1280_240&ut=MuMu_4.4.4_19_Android&apiv=4.0.0.0&appv=195&version=4.0.1.10&life=1533621187&clife=1533621187&hid=E3B7F480004AA387B43C99F3C321CAA6&imsi=0&network=1&location={%22longitude%22:116.403699,%22city-code%22:%22131%22,%22prov%22:%22%E5%8C%97%E4%BA%AC%E5%B8%82%22,%22latitude%22:39.914938,%22county%22:%22%E4%B8%9C%E5%9F%8E%E5%8C%BA%22,%22street%22:%22%E4%B8%AD%E5%8D%8E%E8%B7%AF%22,%22city%22:%22%E5%8C%97%E4%BA%AC%E5%B8%82%22}&sids=868_2172-1023_2548-814_2047-1017_2537-1034_2574-915_2292-1026_2555-1038_2585-908_2269-884_2211-940_2352-949_2371-739_1882'
    while page_num <= page_num_max:
        
        post_dic = {'baijia/listall': {'method': 'get',
                                       'app_id': releaser_id,
                                       '_skip': page_num,
                                       '_limit': '20',
                                       '_timg_cover': '100,150,1000',
                                       'video_type': 'media',
                                       'sort_type': 'sort_by_time'}}

        headers = {'Charset': 'UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; MuMu Build/V417IR) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 haokan/4.0.1.10 (Baidu; P1 4.4.4)/esaeteN_91_4.4.4_uMuM/1015351w/0C14B366AD2664656A4CD5BAB3C48291%7C082397947697800/1/4.0.1.10/195/1',
                   'XRAY-TRACEID': 'b74be6e5-1be0-4b04-9f62-7c116f524bb7',
                   'XRAY-REQ-FUNC-ST-DNS': 'okHttp;1538039956430;0',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Content-Length': '164',
                   'Host': 'sv.baidu.com',
                   'Connection': 'Keep-Alive',
                   'Accept-Encoding': 'gzip',
                   'Cookie': 'BAIDUID=0FD29037A7BFCC0051D2EA95593A7EE1:FG=1; BAIDUZID=lOzvTPOaIXEe7OsZu-O1wAWwzNE5fY9RZotsVv2pvjPHBJOaJk3paZ48CZzB1ioQV0sFX9Hu4C7K_oHkm8HE9QL2XyEzf9cCzUrIjudbuSE8; BAIDUCUID=gi238laR280F82ie_avJ8g81valvaSa3luHx8YuAB88qa-8CgOvlfgaBvt_NP2ijA'}

        get_page = requests.post(releaserUrl, data=post_dic, headers=headers)
        page_dic = get_page.json()


#test

post_dic = {'baijia/listall': {'_limit': '20',
                               '_skip': '1',
                               '_timg_cover': '100,150,1000',
                               'app_id': '1569147786064318',
                               'method': 'get',
                               'sort_type': 'sort_by_time',
                               'video_type': 'media'}}