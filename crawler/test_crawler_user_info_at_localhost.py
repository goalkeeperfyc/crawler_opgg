# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 23:12:48 2018

@author: fangyucheng
"""

from crawler_opgg.utils.trans_format import csv_to_lst_with_headline
from crawler_opgg.crawler.crawler_user_info import user_info

t = csv_to_lst_with_headline('D:/python_code/crawler_opgg/database/match_info.csv')

