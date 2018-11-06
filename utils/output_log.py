# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 14:34:37 2018

@author: fangyucheng
"""


import datetime
import logging

def output_log(page_category, program_info, log_path='F:/program_log/'):
# set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.INFO,
                        format='%(message)s',
                        filename=log_path + program_info + datetime.datetime.now().isoformat()[:10] +'.log',
                        filemode='a')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    log_func = logging.getLogger(page_category)
    return log_func