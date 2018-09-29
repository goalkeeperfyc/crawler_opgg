# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 10:50:13 2018

@author: fangyucheng
"""


from crawler_opgg.utils.trans_format import dic_lst_to_file
from crawler_opgg.utils.connect_with_database import write_lst_into_database


def output_result(result_lst,
                  output_to_mysql=True,
                  database_name='crawler_opgg',
                  table_name='user_info',
                  output_to_file=False,
                  file_name=None):

    if output_to_mysql is True and table_name is not None:
        write_lst_into_database(data_lst=result_lst,
                                database_name=database_name,
                                table_name=table_name)

    if output_to_file is True and file_name is not None:
        dic_lst_to_file(lst_name=result_lst,
                        file_name=file_name)
    else:
        pass
