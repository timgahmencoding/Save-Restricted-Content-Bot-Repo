# SuperFastPython.com
# example of canceling all tasks
from random import random
import asyncio
 
# cancel all running tasks
async def cancel_all_tasks(exclude_list=[]):
    # get all tasks
    all_tasks = asyncio.all_tasks()
    # remove all excluded tasks
    all_tasks = [t for t in all_tasks if t not in exclude_list]
    # enumerate all tasks
    for task in all_tasks:
        # request the task cancel
        task.cancel()
    # wait for all tasks to cancel
    await asyncio.gather(*all_tasks, return_exceptions=True)
 
# task that take a long time
async def work(value):
    try:
        # sleep a long time
        await asyncio.sleep(10 * random())
        print(f'>task {value} done')
    finally:
        # take some time to clean up
        await asyncio.sleep(2 * random())

# main coroutine
async def main():
    # report a message
    print('Main started')
    # issue many tasks
    tasks = [asyncio.create_task(work(i)) for i in range(100)]
    # allow the tasks to run a while
    await asyncio.sleep(4)
    # cancel all tasks
    print('Main canceling all tasks')
    await cancel_all_tasks([asyncio.current_task()])
    # report a message
    print('Main done')
 
# start the event loop
asyncio.run(main())