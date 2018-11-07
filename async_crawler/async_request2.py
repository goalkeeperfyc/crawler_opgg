# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:12:35 2018

@author: fangyucheng
"""


import asyncio
import aiohttp
import time

start = time.time()



async def get(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        result = await response.text()
    return result

async def request():
    url = 'https://api.github.com/events'
    print('Waiting for', url)
    result = await get(url)
    print('Get response from', url)

tasks = [asyncio.ensure_future(request()) for _ in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()
print('Cost time:', end - start)