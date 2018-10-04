# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 01:51:54 2018

@author: goalkeeper
"""

import multiprocessing
import time

def func(msg):
    for i in range(3):
        print (msg)
        time.sleep(1)

if __name__ == "__main__":
    p = multiprocessing.Process(target=func, args=("hello", ))
    p.start()
    p.join()
    print ("Sub-process done.")