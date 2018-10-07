# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 17:01:24 2018

@author: goalkeeper
"""

import argparse
import datetime
from crawler_opgg.utils import trans_format
from crawler_opgg.utils.extract_from_database import extract_data

parse = argparse.ArgumentParser(description='output data from mysql to file')

parse.add_argument('-p', '--path', default='/home/fangyucheng/', type=str,
                   help=("output file's path"))
parse.add_argument('-n', '--name', default='a_failure_attemp', type=str,
                   help=("output file's name"))
parse.add_argument('-a', '--amount', default=None, type=int,
                   help=("the amount of data to extract"))
parse.add_argument('-s', '--sql', default='select * from user_performance', type=str,
                   help=("search sql to extract data"))

args = parse.parse_args()

data_lst = extract_data(search_sql=args.sql,
                        sum_of_data=args.amount,
                        )
print("extract data successfully")
file_name = args.path + args.name

for line in data_lst:
    create_time = datetime.datetime.strftime(line['create_time'], '%Y-%m-%d %H:%M:%S')
    line['create_time'] = create_time

trans_format.dic_lst_to_file(lst_name=data_lst,
                             file_name=file_name)