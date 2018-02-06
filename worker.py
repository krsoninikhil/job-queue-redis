import json
import time
import threading
import sys
from functools import partial

from task_queue import TaskQueue
import tasks

LOGFILE = 'logs.txt'

def clear_logs():
    with open(LOGFILE, 'w') as f:
        f.write('')

def execute_task(task, resources):
    with open(LOGFILE, 'a') as f:
        f.write('{} INFO: Executing task {} from tasks.py with args: {}\n'.format(
            time.time(), task['task'], task['args']))
        status = getattr(tasks, task['task'])(task['args'])
        f.write('{} INFO: Exited with status: {}\n\n'.format(time.time(),
            status))
    # free up the resources
    resources[0] += int(task['args']['resources']['cpu'])
    resources[1] += int(task['args']['resources']['mem'])

def start_worker(channel='tasks', max=None, resources=[]):
    """
    channel: Queue from which tasks needs to be executed
    max: Maximum number of tasks to be exucuted,
        useful when worker is started from another process.
        None (default) means all and keep listening for more
    resources: List of available CPU and memory for the worker
    """

    # initialize worker environment
    clear_logs()
    count = 0
    q = TaskQueue(config_file='config.json')

    # start continuously checking queue for tasks
    while True:
        # check if max tasks are executed
        if max is not None:
            if count < max:
                count += 1
            else:
                break

        task = q.pop()
        if task is not None:
            task = json.loads(task.decode('utf-8'))

            if len(resources) == 2 and \
                resources[0] is not None and resources[1] is not None:
                req_cpu = int(task['args']['resources']['cpu'])
                req_mem = int(task['args']['resources']['mem'])
                # wait if enough resources are not available
                while resources[0] < req_cpu or resources[1] < req_mem:
                    print('Waiting for resources ...')
                    time.sleep(1)
                # grab them as soon as they are available
                resources[0] -= req_cpu
                resources[1] -= req_mem

            # execute the task if resources are available
            p = threading.Thread(
                    target=execute_task, args=(task, resources)
                ).start()
        else:
            # if task queue is empty, wait 1 second before checking again
            count -= 1
            time.sleep(1)
    return 0


if __name__ == '__main__':
    cpu = mem = None
    if len(sys.argv) == 3:
        cpu = sys.argv[1]
        mem = sys.argv[2]
    start_worker(resources=[int(cpu), int(mem)])
