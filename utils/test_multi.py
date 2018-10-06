# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 13:19:23 2018

@author: goalkeeper
"""

from multiprocessing import Pool

import time

 

def fun1(t):
    
    print ('this is fun1',time.ctime())
    
    time.sleep(t)
    
    print ('fun1 finish',time.ctime())

 

def fun2(t):

    print ('this is fun2',time.ctime())
    
    time.sleep(t)
    
    print ('fun2 finish',time.ctime())

 

if __name__ == '__main__':

    a=time.time()

    pool = Pool(processes =3) # 可以同时跑3个进程

    for i in range(3,8):

        pool.apply_async(fun1,(i,))

    pool.close()

    pool.join()

    b=time.time()

    print ('finish',b-a)