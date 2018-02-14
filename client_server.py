# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 19:46:22 2018

@author: glaci
"""

import asyncio
import random
import time

totalTime = 0
start_processing_time = 0
async def client_create_and_send_request(item, queue):
    ranNumber = random.random()
    global totalTime
    totalTime += ranNumber
    print("creating request #%d should take %f seconds to complete" % (item, ranNumber ))
    await asyncio.sleep(ranNumber)
    await queue.put(item)
    
async def server_processing_client_request(  queue ):
    global start_processing_time
    start_processing_time = time.time()
    while True:
        item = await queue.get()
        temp =random.random()
        print("server is processing clinet request... #%d should take %f second to complete. Processing time %f item(s)/sec" %(item , temp, 1/temp))
        await asyncio.sleep(random.random())       
        queue.task_done()
 
async def disPatch(howManyOrderToSend,queue):
    asyncio.ensure_future(server_processing_client_request(queue))
    start_time = time.time()
    
    await asyncio.wait([
            client_create_and_send_request(ele,queue) for ele in range(howManyOrderToSend)
    ])# this is the code that achieves concurrency
    realTime = time.time() - start_time

    print("All client requests sent should have taken %f seconds but instead took only  %f seconds!. Acheived concurrency !!!! " % (totalTime, realTime))
    await queue.join()
  #  server.cancel()
    processTime = howManyOrderToSend / (time.time() - start_processing_time)
    print("Server isn't so lucky there is no concurrency on the server side, avg. processing time:  %f item/second" %(processTime))
    
queue = asyncio.Queue()
loop1 = asyncio.get_event_loop()
loop1.run_until_complete(disPatch(10,queue)) # client will send in 10 requests concurrently
#loop3.close() 


loop1.run_until_complete(disPatch(20,queue))
loop1.run_until_complete(disPatch(100,queue))
loop1.run_until_complete(disPatch(1000,queue))