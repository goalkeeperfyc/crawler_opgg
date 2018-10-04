# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 11:59:32 2018

@author: fangyucheng
"""

import multiprocessing

def worker(num):
    """thread worker function"""
    print ('Worker:', num)
    return

if __name__ == '__main__':
    jobs = []
    for i in range(20):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()