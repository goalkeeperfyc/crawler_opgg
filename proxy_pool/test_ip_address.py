# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:40:51 2018

@author: fangyucheng
"""

import pymysql
import datetime
import requests
from crawler_sys.proxy_pool import connect_with_database


def test_ip_in_raw_database(create_time=None):
    if create_time is None:
        create_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    test_lst = connect_with_database.extract_raw_data_to_test(create_time=create_time)
    result_lst = []
    update_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    for line in test_lst:
        cate = line['category']
        cate = cate.lower()
        ip_address = line['ip_address']
        port = line['port']
        proxy = cate + '://' + ip_address + ':' + port
        proxy_dic = {cate: proxy}
        try:
            get_page = requests.get('http://service.cstnet.cn/ip', proxies=proxy_dic, timeout=8)
            response_time = get_page.elapsed
            after_test_dic = {}
            after_test_dic['whole_ip_address'] = proxy
            after_test_dic['category'] = cate
            after_test_dic['availability'] = 1
            after_test_dic['ip_address'] = ip_address
            after_test_dic['update_time'] = update_time
            result_lst.append(after_test_dic)
            connect_with_database.write_dic_into_database(data_dic=after_test_dic,
                                                          table_name='useful_ip')
            print('%s is useful with response time %s' % (ip_address, response_time))
        except:
            print('%s is not useful' % ip_address)
        connect_with_database.update_status(line)
    return result_lst


def re_test_ip(update_time=None):
    if update_time == None:
        update_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    test_lst = connect_with_database.extract_tested_data_to_test(update_time=update_time)
    connection = pymysql.connect(host='localhost', user='root', passwd='goalkeeper@1',
                                 db='proxy_pool', port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    result_lst = []
    update_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    for line in test_lst:
        proxy_dic = {line['category']: line['whole_ip_address']}
        line_id = line['id']
        try:
            get_page = requests.get(url='http://service.cstnet.cn/ip', proxies=proxy_dic, timeout=15)
            update_sql = "update useful_ip set availability=1 where id=" + str(line_id) 
            cursor.execute(update_sql)
            connection.commit()
            print('this proxy is useful')
        except:
            update_sql = "update useful_ip set availability=0 where id=" + str(line_id) 
            cursor.execute(update_sql)
            connection.commit()
            print('%s is not useful' % proxy_dic)
    update_sql = "update useful_ip set update_time='" + update_time + "' where id>1"
    cursor.execute(update_sql)
    connection.commit()
    return result_lst


if __name__ == '__main__':
    test_ip_in_raw_database()