import json
import time
import threading
from functools import partial

from task_queue import TaskQueue
import tasks

LOGFILE = 'logs.txt'

def clear_logs():
    with open(LOGFILE, 'w') as f:
        f.write('')

def execute_task(task):
    task = json.loads(task.decode('utf-8'))
    with open(LOGFILE, 'a') as f:
        f.write('{} INFO: Executing task {} from tasks.py with args: {}\n'.format(
            time.time(), task['task'], task['args']))
        status = getattr(tasks, task['task'])(task['args'])
        f.write('{} INFO: Exited with status: {}\n\n'.format(time.time(),
            status))

def start_worker(channel='tasks', max=None):
    """
    channel: queue from which tasks needs to be executed
    max: maximum number of tasks to be exucuted,
         None (default) means all and keep listening for more
    """
    q = TaskQueue(config_file='config.json')
    count = 0
    clear_logs()
    while True:
        # check if max tasks are executed
        if max is not None:
            if count < max:
                count += 1
            else:
                break

        task = q.pop()
        if task is not None:
             p = threading.Thread(target=execute_task, args=(task,)).start()
        else:
            # if task queue is empty, wait 1 second before checking again
            count -= 1
            time.sleep(1)
    return 0
