# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 11:59:32 2018

@author: fangyucheng
"""

import multiprocessing

def worker(num):
    """thread worker function"""
    open_file = open('/home/fangyucheng/test_multiprocessing', 'a')
    open_file.write(str(num))
    open_file.write('\n')
    open_file.flush()
    open_file.close()


for i in range(20):
    p = multiprocessing.Process(target=worker, args=(i,))
    print(type(p))
    p.start()